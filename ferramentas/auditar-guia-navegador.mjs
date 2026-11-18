// Auditoria no navegador do guia: reflow em 320 px, teste interativo de TODAS as questões e axe-core.
//
// Uso (Node 18+; Playwright e axe-core instalados fora do projeto):
//   node ferramentas/auditar-guia-navegador.mjs \
//     --guia /caminho/guia-engenharia-llms.html \
//     --playwright /caminho/node_modules/playwright \
//     --axe /caminho/node_modules/axe-core/axe.min.js \
//     --chrome /caminho/chrome
// Saída: JSON com reflow, questões e axe; código de saída 1 se houver falha.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';

const arg = (nome) => {
  const i = process.argv.indexOf(`--${nome}`);
  if (i < 0 || !process.argv[i + 1]) { console.error(`falta --${nome}`); process.exit(2); }
  return process.argv[i + 1];
};
const guia = path.resolve(arg('guia'));
const require = createRequire(import.meta.url);
const { chromium } = require(path.resolve(arg('playwright')));
const axeSource = fs.readFileSync(path.resolve(arg('axe')), 'utf8');
const url = 'file://' + guia;
const browser = await chromium.launch({ executablePath: path.resolve(arg('chrome')), headless: true });
let falhas = 0;

try {
  // 1. Reflow em 320 px + teste interativo de todas as questões (uma alternativa por questão, alternando A–D)
  const p320 = await browser.newPage({ viewport: { width: 320, height: 640 } });
  const erros = [];
  p320.on('pageerror', (e) => erros.push(e.message));
  await p320.goto(url, { waitUntil: 'load' });

  const reflow = await p320.evaluate(() => {
    const vw = window.innerWidth;
    const dentroDeRolagem = (el) => {
      for (let c = el; c && c !== document.body; c = c.parentElement) {
        if (c.classList && c.classList.contains('rolagem')) return true;
        if (c.tagName === 'PRE') return true;
      }
      return false;
    };
    const estouros = [];
    for (const el of document.querySelectorAll('body *')) {
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden' || dentroDeRolagem(el)) continue;
      const r = el.getBoundingClientRect();
      if (!r.width && !r.height) continue;
      if (r.right > vw + 0.5 || r.left < -0.5) {
        estouros.push({ tag: el.tagName.toLowerCase(), id: el.id, texto: (el.textContent || '').trim().slice(0, 40) });
      }
    }
    return {
      docClient: document.documentElement.clientWidth,
      docScroll: document.documentElement.scrollWidth,
      bodyScroll: document.body.scrollWidth,
      secoes: document.querySelectorAll('section.page').length,
      estouros: estouros.slice(0, 20),
      totalEstouros: estouros.length,
    };
  });
  if (reflow.docScroll !== 320 || reflow.bodyScroll !== 320 || reflow.totalEstouros) falhas++;

  const questoes = await p320.evaluate(() => {
    const falhasQ = [];
    let total = 0, acertos = 0, erradas = 0;
    const fieldsets = Array.from(document.querySelectorAll('fieldset.questao'));
    fieldsets.forEach((fs, i) => {
      const radios = Array.from(fs.querySelectorAll('input[type="radio"]'));
      const nome = radios[0] && radios[0].name;
      if (radios.length !== 4) { falhasQ.push({ nome, motivo: 'alternativas != 4' }); return; }
      const alvo = radios[i % 4];
      const correta = radios.find((r) => r.dataset.correta === 'true');
      alvo.click();
      total++;
      const retorno = fs.querySelector('.retorno');
      const txt = (retorno.textContent || '').trim();
      const esperado = alvo === correta ? 'Correto.' : 'Incorreto.';
      if (alvo === correta) acertos++; else erradas++;
      if (!txt.startsWith(esperado)) falhasQ.push({ nome, motivo: 'veredito errado', txt: txt.slice(0, 60) });
      if (alvo !== correta) {
        const letra = correta.closest('label').querySelector('strong').textContent;
        if (!txt.includes('Alternativa correta: ' + letra)) falhasQ.push({ nome, motivo: 'letra correta ausente' });
      }
      if (retorno.getAttribute('aria-live') !== 'polite' || retorno.getAttribute('role') !== 'status') falhasQ.push({ nome, motivo: 'região aria-live ausente' });
      if (radios.filter((r) => !r.disabled).length !== 1) falhasQ.push({ nome, motivo: 'alternativas não travadas' });
    });
    return { total, acertos, erradas, falhas: falhasQ };
  });
  if (questoes.falhas.length || !questoes.total) falhas++;
  if (erros.length) falhas++;
  await p320.close();

  // 2. axe-core em 1280×800 e 320×640
  const axe = {};
  for (const [nome, vp] of [['1280x800', { width: 1280, height: 800 }], ['320x640', { width: 320, height: 640 }]]) {
    const pg = await browser.newPage({ viewport: vp });
    await pg.goto(url, { waitUntil: 'load' });
    await pg.addScriptTag({ content: axeSource });
    axe[nome] = await pg.evaluate(async () => {
      const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'] } });
      return {
        passes: r.passes.length,
        violations: r.violations.map((v) => ({ id: v.id, nos: v.nodes.length, amostra: v.nodes.slice(0, 3).map((n) => n.html.slice(0, 100)) })),
        incomplete: r.incomplete.map((v) => ({ id: v.id, nos: v.nodes.length, amostra: v.nodes.slice(0, 3).map((n) => n.html.slice(0, 100)) })),
      };
    });
    if (axe[nome].violations.length) falhas++;
    await pg.close();
  }

  console.log(JSON.stringify({ reflow, questoes, axe, errosDePagina: erros, falhas }, null, 2));
} finally {
  await browser.close();
}
process.exit(falhas ? 1 : 0);
