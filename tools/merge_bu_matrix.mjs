import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const MATRIX = path.resolve(ROOT, "..", "edi-bre-bu-business-rules-matrix.html");
const INDEX = path.join(ROOT, "index.html");

function extractMatrixBody(html) {
  const m = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (!m) throw new Error("No body in matrix");
  return m[1].trim();
}

function localizeTablesForEs(fragment) {
  return fragment
    .replace(
      /Central tracking \(companion capability\)/g,
      "Seguimiento central (capacidad complementaria)"
    )
    .replace(
      /Programme-level notes \(not BU data prerequisites\)/g,
      "Notas de programa (no son prerrequisitos de datos BU)"
    )
    .replace(
      /HLR page IDs \(BLK\) used in this matrix/g,
      "IDs de página HLR (BLK) citados en esta matriz"
    )
    .replace(
      /Visibility &amp; ops actions — not a BRE validation rule/g,
      "Visibilidad y acciones de ops — no es una regla de validación del BRE"
    )
    .replace(/>Business rule</g, ">Regla de negocio<")
    .replace(/>Capability</g, ">Capacidad<")
    .replace(
      />Short description<span class="th-hint">Business “what” — intent in plain language\.<\/span>/g,
      '>Descripción corta<span class="th-hint">Qué de negocio — intención en lenguaje claro.</span>'
    )
    .replace(
      />Scope<span class="th-hint">What is evaluated and how the application behaves \(steps, fallbacks, outcomes\)\.<\/span>/g,
      '>Alcance<span class="th-hint">Qué se evalúa y cómo se comporta la aplicación (pasos, alternativas, resultados).</span>'
    )
    .replace(
      />Prerequisites<span class="th-hint">BU-owned master data &amp; ingestion so BRE can execute the rule\.<\/span>/g,
      '>Prerrequisitos<span class="th-hint">Datos maestros e ingesta a cargo de la BU para ejecutar la regla.</span>'
    )
    .replace(
      />Short description<span class="th-hint">Business “what”\.<\/span>/g,
      '>Descripción corta<span class="th-hint">Qué de negocio.</span>'
    )
    .replace(
      />Scope<span class="th-hint">How it works\.<\/span>/g,
      '>Alcance<span class="th-hint">Cómo funciona.</span>'
    )
    .replace(
      />Prerequisites<span class="th-hint">BU \/ partner data &amp; ownership\.<\/span>/g,
      '>Prerrequisitos<span class="th-hint">Datos de BU / partner y titularidad.</span>'
    );
}

const matrixHtml = fs.readFileSync(MATRIX, "utf8");
const body = extractMatrixBody(matrixHtml);

const enSection =
  '<section class="slide slide--bre-matrix" id="section-tech-bu-matrix">\n' +
  '                <p class="slide-num">Technical · BU scope &amp; prerequisites matrix</p>\n' +
  '                <div class="bre-bu-matrix">\n' +
  body +
  "\n                </div>\n" +
  "</section>\n";

const ts = body.indexOf('<div class="table-scroll">');
const tablesFragment = ts >= 0 ? body.slice(ts) : "";
const tablesFragmentEs = localizeTablesForEs(tablesFragment);

const esSection =
  `
<section class="slide slide--bre-matrix" id="section-tech-bu-matrix-es">
                <p class="slide-num">Técnico · Matriz BU</p>
                <div class="bre-bu-matrix">
                    <div class="hero">
                        <svg class="hex" viewBox="0 0 100 100" aria-hidden="true"><polygon points="25,2 75,2 100,50 75,98 25,98 0,50" fill="#FFC000"/></svg>
                        <div class="in">
                            <div class="brandmark"><span class="dot"></span> BEES Link</div>
                            <div class="kicker">EDI · Motor de reglas de negocio (BRE)</div>
                            <h1>Reglas de negocio — alcance BU y prerrequisitos</h1>
                            <p>Vista única para stakeholders: cada fila separa la <strong>intención de negocio</strong> (descripción corta), el <strong>comportamiento del producto</strong> (alcance) y las <strong>obligaciones de datos maestros de la BU</strong> (prerrequisitos). Alineado a <strong>HLR</strong> BLK (carpetas 1ª / 2ª / 3ª capa y Central Tracking). Si el resumen ejecutivo difiere, <strong>prevalece el HLR</strong>.</p>
                            <div class="hero meta">
                                <span><b>Audiencia:</b> Producto · Operaciones · Finanzas · TI · Líderes de mercado</span>
                                <span><b>Fuente primaria:</b> <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/folder/5769003728" style="color:#e0e0e0">BLK — árbol EDI BRE</a></span>
                                <span><b>Detalle de celdas:</b> en inglés (texto HLR)</span>
                                <span><b>Actualizado:</b> sep 2026</span>
                            </div>
                        </div>
                    </div>
                    <div class="wrap">
                        <h2>Cómo usar esta matriz</h2>
                        <div class="lead">Una fila por regla — tres columnas.</div>
                        <div class="card accent">
                            <h3>Qué significa cada columna</h3>
                            <p><strong>Descripción corta</strong> — El &quot;qué&quot; de negocio en lenguaje claro.</p>
                            <p><strong>Alcance</strong> — Qué evalúa el producto y <strong>cómo se comporta</strong>.</p>
                            <p><strong>Prerrequisitos</strong> — Qué debe garantizar la <strong>BU en datos e ingesta</strong>.</p>
                        </div>
                        <div class="pull"><b>Checklist de firma:</b> BU atestigua <b>Prerrequisitos</b>. Producto + ops atestiguan <b>Alcance</b>. Comercial / finanzas atestiguan <b>Descripción corta</b> cuando aplique.</div>
                        <p class="draft-note">Las tablas siguientes conservan el texto de celda en inglés (citas HLR). Encabezados de tabla localizados donde aplica.</p>
                        <h2>Matriz — reglas de validación</h2>
                        <div class="lead">Regla · descripción corta · alcance · prerrequisitos</div>
                        <p class="draft-note">Incluye HLR de tercera capa (MOQ, MAX, SKU) y Central Tracking Phase 2. Texto de celdas en inglés (citas HLR).</p>
                        ${tablesFragmentEs}
                    </div>
                </div>
</section>
`.trim() + "\n";

let idx = fs.readFileSync(INDEX, "utf8");
idx = idx.replace(/\r\n/g, "\n");

const force = process.argv.includes("--force");

const reEn =
  /<section class="slide slide--bre-matrix" id="section-tech-bu-matrix">[\s\S]*?<\/section>\n(?=<section class="slide" id="section-tech-overview">)/;
const reEs =
  /<section class="slide slide--bre-matrix" id="section-tech-bu-matrix-es">[\s\S]*?<\/section>\n(?=<section class="slide" id="section-tech-overview-es">)/;

if (idx.includes('id="section-tech-bu-matrix"') && !force) {
  console.log("Skip: section-tech-bu-matrix already present (use --force to replace)");
  process.exit(0);
}

if (force) {
  if (!reEn.test(idx)) throw new Error("EN matrix section not found for --force");
  if (!reEs.test(idx)) throw new Error("ES matrix section not found for --force");
  idx = idx.replace(reEn, enSection);
  idx = idx.replace(reEs, esSection);
} else {
  const markerEn =
    '            <div class="doc-i18n doc-i18n--en" data-doc-lang="en">\n<section class="slide" id="section-tech-overview">';
  const markerEs =
    '            <div class="doc-i18n doc-i18n--es" data-doc-lang="es">\n<section class="slide" id="section-tech-overview-es">';
  if (!idx.includes(markerEn)) throw new Error("EN marker not found");
  if (!idx.includes(markerEs)) throw new Error("ES marker not found");
  idx = idx.replace(
    markerEn,
    "            <div class=\"doc-i18n doc-i18n--en\" data-doc-lang=\"en\">\n" +
      enSection +
      '<section class="slide" id="section-tech-overview">'
  );
  idx = idx.replace(
    markerEs,
    "            <div class=\"doc-i18n doc-i18n--es\" data-doc-lang=\"es\">\n" +
      esSection +
      '<section class="slide" id="section-tech-overview-es">'
  );
}

fs.writeFileSync(INDEX, idx.replace(/\n/g, "\r\n"), "utf8");
console.log("OK: merged matrix into", INDEX);
