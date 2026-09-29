#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..');
const targets = [
  path.join(root, 'index.html'),
  path.join(root, 'EDI-Order-Validation-Scope_Exec_Summary-v1.1.html'),
];

const CONFLICT_RE = /<<<<<<< HEAD\r?\n([\s\S]*?)=======\r?\n([\s\S]*?)>>>>>>> abinbev\/main\r?\n/g;

function resolveConflict(head, main) {
  const h = head.trimEnd();
  const m = main.trimEnd();

  if (h.includes('<b>Context:</b>') && m.includes('BU decisions timeline')) {
    return `      <span><b>Context:</b> <a href="https://silarerenan-cmyk.github.io/edi-bre-exec-summary/" style="color:#e0e0e0">Exec summary</a> (orientation only)</span>
      <span><b>Updated:</b> Sep 2026</span>
      <span><b>Related:</b> <a href="bu-decisions-timeline.html" style="color:#FFC000">BU decisions timeline</a> (definitions &amp; stakeholder sign-offs)</span>
`;
  }
  if (h.includes('Detalle de celdas') && m.includes('Línea de tiempo')) {
    return `                                <span><b>Detalle de celdas:</b> en inglés (texto HLR)</span>
                                <span><b>Columnas comerciales:</b> BUs, riesgo y ETA en español</span>
                                <span><b>Actualizado:</b> sep 2026</span>
                                <span><b>Relacionado:</b> <a href="bu-decisions-timeline.html" style="color:#FFC000">Línea de tiempo de decisiones BU</a> (definiciones y sign-offs)</span>
`;
  }
  if (h.includes('Business rule · short description') && m.includes('related BUs')) {
    return `<div class="lead">Business rule · related BUs · short description · scope · prerequisites · risk · ETA</div>
<p class="draft-note">Description, scope, and prerequisites aligned to published <strong>BLK</strong> HLRs (3rd-layer MOQ/MAX/SKU included). <strong>Related BUs</strong>, <strong>risk</strong>, and <strong>ETA</strong> merged from the commercial feasibility one-pager. <strong>Central Tracking</strong> is not a validator rule — see the companion table after this one.</p>

`;
  }
  if (h.includes('Regla · descripción corta') && m.includes('Regla · BUs')) {
    return `                        <div class="lead">Regla · BUs · descripción corta · alcance · prerrequisitos · riesgo · ETA</div>
                        <p class="draft-note">Descripción, alcance y prerrequisitos alineados a HLR BLK (MOQ/MAX/SKU de tercera capa incluidos). <strong>BUs relacionadas</strong>, <strong>riesgo</strong> y <strong>ETA</strong> fusionados desde el one-pager de viabilidad comercial. <strong>Central Tracking</strong> no es regla del validador — ver tabla complementaria.</p>

`;
  }
  if (h.includes('<b>UPC matching</b>') && m.includes('<b>UPC matching</b>')) {
    return `      <td><b>UPC matching</b><span class="hlr-ref">BEESEDI-48947 · BEESEDI-53722 · BEESEDI-53692</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span></div></td>
      <td>Resolve each line’s retailer product code to exactly one BEES item, using the catalogue first and POC-level mappings only as a fallback — so later rules always see a stable <code>beesItemId</code>. Implementation splits across strict catalog path (<a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6140789875">48947</a>), POC mapping fallback (<a href="https://ab-inbev.atlassian.net/browse/BEESEDI-53722">53722</a>), and PO Reader curated lookup (<a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6357876913">53692</a>).</td>
`;
  }
  if (h.includes('<b>Package validation</b>') && m.includes('zone-badge')) {
    return `      <td><b>Package validation</b><span class="hlr-ref">BEESEDI-48954</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span></div></td>
      <td>Convert each line’s retailer quantity to ABI <strong>billing boxes</strong> using <code>pack_conversion_factor</code> per SKU + commercial scope (<code>zoneChainId</code>) — without trusting retailer-declared UOM on the EDI line.</td>
`;
  }
  if (h.includes('BEESEDI-54950') && m.includes('Tax validation')) {
    const es = m.includes('Asegurar');
    if (es) {
      return `      <td><b>Tax validation</b><span class="hlr-ref">Exec summary · New</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span></div></td>
      <td>Asegurar que se aplican los impuestos correctos por región del POC antes de completar las compuertas a nivel ítem, alineado al modelo de pricing de BEES.</td>
      <td>
        <ol style="margin:0;padding-left:1.2em">
          <li>Tras validación de precio, evaluar configuración fiscal por línea según reglas de región del POC en BEES.</li>
          <li>Impuesto incorrecto -> <strong>bloquear o rechazar</strong> según configuración país+vendor (entrega con squad Pricing Q3).</li>
          <li>Toggle <strong>por país + vendor</strong>; omitido si está desactivado.</li>
`;
    }
    return `      <td><b>Tax validation</b><span class="hlr-ref">Exec summary · New</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span></div></td>
      <td>Ensure the correct taxes are applied per POC region before item-level gates complete, aligned with the BEES pricing model.</td>
      <td>
        <ol style="margin:0;padding-left:1.2em">
          <li>After price validation, evaluate tax configuration for each line against POC region rules in BEES.</li>
          <li>Incorrect tax application -> <strong>block or reject</strong> per country+vendor configuration (delivery with Pricing squad Q3).</li>
          <li>Toggle <strong>per country + vendor</strong>; skipped when disabled.</li>
`;
  }
  if (h.includes('vendor catalog + zone stock') && m.includes('tax rules')) {
    const es = m.includes('Finanzas');
    if (es) {
      return `          <li>Finanzas provee <strong>reglas / configuración fiscal por región del POC</strong> alineada al modelo de pricing BEES.</li>
`;
    }
    return `          <li>Finance provides <strong>tax rules / configuration per POC region</strong> aligned with BEES pricing model.</li>
`;
  }
  if (h.includes('BEESEDI-54948') && m.includes('SKU availability</b></td>')) {
    const es = m.includes('Validate if the SKUs');
    const skuTail = es
      ? `      <td><b>SKU availability</b><span class="hlr-ref">BEESEDI-54950</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span><span class="zone-badge zone-badge--ar">AR</span></div></td>
      <td>Validate each resolved line’s requested quantity against BEES stock via the same cart-validation path as checkout — adjusting, dropping, or keeping lines so fill rate is predictable.</td>
      <td>
        <ol style="margin:0;padding-left:1.2em">
          <li>Runs <strong>after UPC matching</strong> (and sibling line-level prerequisites) for lines with a single resolved SKU. Toggle <code>SKU_AVAILABILITY</code> + retailer blacklist.</li>
          <li>Call <strong>cart-validation / pricing simulation</strong> (Stepper <code>PERFORM_CARTS_VALIDATION</code>); BRE <strong>consumes</strong> outcomes — no duplicate stock engine.</li>
          <li>Sufficient stock → accept line; partial stock → <strong>adjust quantity</strong> when policy allows; zero stock → <strong>drop line</strong>. Order becomes <strong>Partially accepted</strong> when some lines survive; <strong>Rejected</strong> when no lines remain.</li>
`
      : `      <td><b>SKU availability</b><span class="hlr-ref">BEESEDI-54950</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span><span class="zone-badge zone-badge--ar">AR</span></div></td>
      <td>Validate each resolved line’s requested quantity against BEES stock via the same cart-validation path as checkout — adjusting, dropping, or keeping lines so fill rate is predictable.</td>
      <td>
        <ol style="margin:0;padding-left:1.2em">
          <li>Runs <strong>after UPC matching</strong> (and sibling line-level prerequisites) for lines with a single resolved SKU. Toggle <code>SKU_AVAILABILITY</code> + retailer blacklist.</li>
          <li>Call <strong>cart-validation / pricing simulation</strong> (Stepper <code>PERFORM_CARTS_VALIDATION</code>); BRE <strong>consumes</strong> outcomes — no duplicate stock engine.</li>
          <li>Sufficient stock → accept line; partial stock → <strong>adjust quantity</strong> when policy allows; zero stock → <strong>drop line</strong>. Order becomes <strong>Partially accepted</strong> when some lines survive; <strong>Rejected</strong> when no lines remain.</li>
`;
    return skuTail;
  }
  if (h.includes('minimum order configuration') && m.includes('BEES ATP')) {
    const es = m.includes('inventario');
    if (es) {
      return `          <li>BUs keep vendor catalog + zone stock configuration aligned with warehouse ATP and cut-offs (same source as app checkout).</li>
          <li>Inventory enforcement modules in cart-service remain source of truth for partial vs reject behaviour.</li>
          <li><strong>APIs de ingesta de datos:</strong> <a href="https://developer.bees-platform.com/docs/entities/inventory/api/v3/post" target="_blank" rel="noopener noreferrer">Inventory API v3 (POST)</a></li>
`;
    }
    return `          <li>BUs keep vendor catalog + zone stock configuration aligned with warehouse ATP and cut-offs (same source as app checkout).</li>
          <li>Inventory enforcement modules in cart-service remain source of truth for partial vs reject behaviour.</li>
          <li><strong>Data ingestion APIs:</strong> <a href="https://developer.bees-platform.com/docs/entities/inventory/api/v3/post" target="_blank" rel="noopener noreferrer">Inventory API v3 (POST)</a></li>
`;
  }
  if (h.includes('BEESEDI-54948') && m.includes('Minimum order quantity</b></td>')) {
    return `      <td><b>Minimum order quantity</b><span class="hlr-ref">BEESEDI-54948</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span><span class="zone-badge zone-badge--ar">AR</span></div></td>
      <td>Enforce store-level minimum order thresholds on the <strong>validated order aggregate</strong> using cart-service evaluation — rejecting sub-minimum EDI orders that app checkout would block.</td>
      <td>
        <ol style="margin:0;padding-left:1.2em">
          <li><strong>Stage 3</strong> order-level gate after line-level rules. Toggle per country + vendor; retailer blacklist skips rule.</li>
          <li>Consult cart-validation for MOQ type (quantity, subtotal, full price, etc.). Unconfigured store → <strong>skip</strong>. Below minimum → <strong>reject entire order</strong> (label <em>Minimum order quantity</em>) — <strong>no multi-order hold / combine window</strong> in MVP.</li>
          <li>MX: skip for <strong>T4 pickup</strong> and <strong>CEDIS</strong> channel orders. AR remote billing Flow 2 → <strong>skipped</strong>.</li>
`;
  }
  if (h.includes('maximum order</strong> rows') && m.includes('minimum order quantity</strong> configured')) {
    return `          <li>BUs maintain minimum order configuration in Global Accounts / store overrides (Accounts Relay V2 + BEES Sync).</li>
          <li>Commercial agrees canonical rejection messaging surfaced in Central Tracking.</li>
          <li><strong>Data ingestion APIs:</strong> <a href="https://developer.bees-platform.com/docs/entities/accounts/csv/v2/post" target="_blank" rel="noopener noreferrer">Accounts CSV v2 (POST)</a></li>
`;
  }
  if (h.includes('BEESEDI-54949') && m.includes('Minimum order quantity</b></td>')) {
    return `      <td><b>Maximum order quantity</b><span class="hlr-ref">BEESEDI-54949</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span></div></td>
      <td>Cap the validated order aggregate against store-level maximum thresholds (MX MVP) via cart-validation — protecting logistics capacity and stock allocation.</td>
      <td>
        <ol style="margin:0;padding-left:1.2em">
          <li><strong>Stage 3</strong> order-level gate; same toggle / blacklist pattern as MOQ. Unconfigured store → <strong>skip</strong>.</li>
          <li>Above maximum → <strong>reject entire order</strong> (<em>Maximum order quantity</em>). At or below → continue to order creation.</li>
          <li>MX: skip for <strong>T4</strong> and <strong>CEDIS</strong>. Markets beyond MX are out of scope for this HLR unless extended later.</li>
`;
  }
  if (h.includes('maximum order</strong> rows') && m.includes('maximum order quantity</strong> configured')) {
    return `          <li>BUs keep <strong>maximum order</strong> rows accurate per POC/vendor in BEES account structures.</li>
          <li>Finance validates monetary vs quantity-based max types match commercial policy.</li>
          <li><strong>Data ingestion APIs:</strong> <a href="https://developer.bees-platform.com/docs/entities/accounts/csv/v2/post" target="_blank" rel="noopener noreferrer">Accounts CSV v2 (POST)</a></li>
`;
  }
  if (h.includes('HLR page IDs (BLK)') && m === '') {
    return `<div class="card">
  <h3>HLR page IDs (BLK) used in this matrix</h3>
  <p style="font-size:14px;margin:0">Order integration <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5981536297">5981536297</a> · POC direct <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5791453558">5791453558</a> · POC external IDs <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6220054719">6220054719</a> · Delivery dates (range + frequency) <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5791453572">5791453572</a> · PO uniqueness <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5792306185">5792306185</a> · UPC matching <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6140789875">6140789875</a> · PO Reader curated lookup <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6357876913">6357876913</a> · Package validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6219956551">6219956551</a> · Price validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6217368312">6217368312</a> · DC validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6222381057">6222381057</a> · MOQ <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6453461458">6453461458</a> · MAX <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6452871508">6452871508</a> · SKU availability <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6452150787">6452150787</a> · Central tracking retailer <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6220185829">6220185829</a> · Central tracking ops <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6218907975">6218907975</a> · Central tracking Phase 2 <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6611174016">6611174016</a></p>
</div>

`;
  }
  if (h.includes('IDs de página HLR') && m === '') {
    return `<div class="card">
  <h3>IDs de página HLR (BLK) citados en esta matriz</h3>
  <p style="font-size:14px;margin:0">Order integration <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5981536297">5981536297</a> · POC direct <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5791453558">5791453558</a> · POC external IDs <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6220054719">6220054719</a> · Delivery dates (range + frequency) <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5791453572">5791453572</a> · PO uniqueness <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5792306185">5792306185</a> · UPC matching <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6140789875">6140789875</a> · PO Reader curated lookup <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6357876913">6357876913</a> · Package validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6219956551">6219956551</a> · Price validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6217368312">6217368312</a> · DC validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6222381057">6222381057</a> · MOQ <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6453461458">6453461458</a> · MAX <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6452871508">6452871508</a> · SKU availability <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6452150787">6452150787</a> · Central tracking retailer <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6220185829">6220185829</a> · Central tracking ops <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6218907975">6218907975</a> · Central tracking Phase 2 <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6611174016">6611174016</a></p>
</div>

`;
  }
  if (h.includes('HLR page IDs') && m.includes('via MCP')) {
    return `<div class="card">
  <h3>HLR page IDs (BLK) used in this matrix</h3>
  <p style="font-size:14px;margin:0">Order integration <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5981536297">5981536297</a> · POC direct <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5791453558">5791453558</a> · POC external IDs <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6220054719">6220054719</a> · Delivery dates (range + frequency) <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5791453572">5791453572</a> · PO uniqueness <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/5792306185">5792306185</a> · UPC matching <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6140789875">6140789875</a> · PO Reader curated lookup <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6357876913">6357876913</a> · Package validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6219956551">6219956551</a> · Price validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6217368312">6217368312</a> · DC validation <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6222381057">6222381057</a> · MOQ <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6453461458">6453461458</a> · MAX <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6452871508">6452871508</a> · SKU availability <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6452150787">6452150787</a> · Central tracking retailer <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6220185829">6220185829</a> · Central tracking ops <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6218907975">6218907975</a> · Central tracking Phase 2 <a href="https://ab-inbev.atlassian.net/wiki/spaces/BLK/pages/6611174016">6611174016</a></p>
</div>

<footer>
  BEES / AB InBev — internal alignment. Visual tokens: BEES Link one-pager reference. Validation matrix updated from <strong>Atlassian Confluence BLK</strong> HLRs for EDI order validator MVP (layers 1–3) + Central Tracking companion capabilities. Executive summary retained only for macro context. Not a legal or contractual substitute for signed HLRs in Jira/Confluence.
`;
  }

  console.warn('Unresolved conflict, keeping HEAD:\n', h.slice(0, 120), '...');
  return head;
}

let html = fs.readFileSync(targets[0], 'utf8');
let prev;
do {
  prev = html;
  html = html.replace(CONFLICT_RE, (_, head, main) => resolveConflict(head, main));
} while (html !== prev && html.includes('<<<<<<< HEAD'));

// Remove duplicate legacy MAX rows (old TBD rows after MOQ)
html = html.replace(
  /    <tr>\n      <td><b>Maximum order quantity<\/b><\/td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX<\/span><\/div><\/td>\n      <td>Validate whether the purchased quantity respects the maximum order quantity[\s\S]*?<span class="tbd-note">\*HLR TBD<\/span><\/td><\/tr>\n/g,
  ''
);

// Fix Phase 2 CT row if still broken (no zone-badges td)
html = html.replace(
  /    <tr>\n      <td><b>Central tracking — Phase 2 line &amp; SKU resolution<\/b><span class="hlr-ref">BEESEDI-57198<\/span><\/td>\n      <td>Extend ops tooling/g,
  `    <tr>
      <td><b>Central tracking — Phase 2 line &amp; SKU resolution</b><span class="hlr-ref">BEESEDI-57198</span></td><td><div class="zone-badges"><span class="zone-badge zone-badge--mx">MX</span><span class="zone-badge zone-badge--ar">AR</span></div></td>
      <td>Extend ops tooling`
);

// Add risk/eta to Phase 2 if row ends without them
html = html.replace(
  /(<td><b>Central tracking — Phase 2 line &amp; SKU resolution<\/b>[\s\S]*?<li>Platform exposes stable line diagnostics and rule codes from BRE logging\.<\/li>\n        <\/ul>\n      <\/td>)\n    <\/tr>/g,
  `$1
      <td class="risk risk--med">No line-level resolution path → partially accepted orders stall in ops backlog.</td><td><span class="eta-bu">BU: Q4 2026</span><br><span class="eta-bre">BRE: Q4 2026</span></td>
    </tr>`
);

if (html.includes('<<<<<<< HEAD')) {
  const n = (html.match(/<<<<<<< HEAD/g) || []).length;
  console.error('Still has conflicts:', n);
  process.exit(1);
}

for (const file of targets) {
  fs.writeFileSync(file, html, 'utf8');
  console.log('Fixed:', file);
}
