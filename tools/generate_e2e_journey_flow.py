#!/usr/bin/env python3
"""Generate detailed E2E journey flow HTML (EN + ES) into index.html markers."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

MARKER_EN_START = "<!-- E2E_JOURNEY_FLOW_EN_START -->"
MARKER_EN_END = "<!-- E2E_JOURNEY_FLOW_EN_END -->"
MARKER_ES_START = "<!-- E2E_JOURNEY_FLOW_ES_START -->"
MARKER_ES_END = "<!-- E2E_JOURNEY_FLOW_ES_END -->"


def arrow() -> str:
    return (
        '<div class="edi-if-row edi-if-row--arrow" aria-hidden="true">'
        '<div class="edi-if-cell edi-if-cell--graph"><div class="edi-vi-arrow"></div></div></div>'
    )


def layer_band(text: str) -> str:
    return f'<div class="edi-if-layer-band">{text}</div>'


def bre_step(
    num: str,
    title: str,
    sub: str,
    note_side: str,
    note_title: str,
    note_desc: str,
    note_left: bool,
    node_class: str = "edi-vi-node--bre",
) -> str:
    row_class = "edi-if-row edi-if-row--note-left" if note_left else "edi-if-row edi-if-row--note-right"
    graph = (
        f'<div class="edi-vi-node {node_class}">'
        f'<span class="edi-vi-bubble">{num}</span>'
        f'<span class="edi-vi-lbl">{title}</span>'
        f'<span class="edi-vi-lbl-sub">{sub}</span></div>'
    )
    note = (
        f'<div class="edi-if-cell edi-if-cell--note-side">'
        f'<strong class="edi-if-ls-title">{note_title}</strong>'
        f'<p class="edi-if-ls-desc">{note_desc}</p></div>'
    )
    if note_left:
        cells = note + f'<div class="edi-if-cell edi-if-cell--graph">{graph}</div>'
    else:
        cells = f'<div class="edi-if-cell edi-if-cell--graph">{graph}</div>' + note
    return f'<div class="{row_class}">{cells}</div>'


def service_step(
    title: str,
    sub: str,
    svc_class: str,
    comm: str,
    note_title: str,
    note_desc: str,
    note_left: bool,
) -> str:
    row_class = "edi-if-row edi-if-row--note-left" if note_left else "edi-if-row edi-if-row--note-right"
    graph = (
        f'<div class="edi-vi-node {svc_class}">'
        f'<span class="edi-vi-bubble edi-vi-bubble--call">↔</span>'
        f'<span class="edi-vi-lbl">{title}</span>'
        f'<span class="edi-vi-lbl-sub">{sub}</span>'
        f'<span class="edi-vi-comm">{comm}</span></div>'
    )
    note = (
        f'<div class="edi-if-cell edi-if-cell--note-side">'
        f'<strong class="edi-if-ls-title">{note_title}</strong>'
        f'<p class="edi-if-ls-desc">{note_desc}</p></div>'
    )
    if note_left:
        cells = note + f'<div class="edi-if-cell edi-if-cell--graph">{graph}</div>'
    else:
        cells = f'<div class="edi-if-cell edi-if-cell--graph">{graph}</div>' + note
    return f'<div class="{row_class} edi-if-row--svc">{cells}</div>'


def diamond(question: str, note_title: str, note_desc: str, note_left: bool) -> str:
    row_class = "edi-if-row edi-if-row--note-left edi-if-row--diamond" if note_left else "edi-if-row edi-if-row--note-right edi-if-row--diamond"
    d = f'<div class="edi-vi-diamond">{question}</div>'
    note = (
        f'<div class="edi-if-cell edi-if-cell--note-side">'
        f'<strong class="edi-if-ls-title">{note_title}</strong>'
        f'<p class="edi-if-ls-desc">{note_desc}</p></div>'
    )
    if note_left:
        cells = note + f'<div class="edi-if-cell edi-if-cell--graph">{d}</div>'
    else:
        cells = f'<div class="edi-if-cell edi-if-cell--graph">{d}</div>' + note
    return f'<div class="{row_class}">{cells}</div>'


def fork(no_label: str, no_pill: str, yes_label: str, yes_pill: str, no_note: str, yes_note: str) -> str:
    return f"""
<div class="edi-if-row edi-if-row--fork-split edi-poc-fork">
    <div class="edi-if-cell edi-if-cell--fork-note-no"><p class="edi-if-fork-note">{no_note}</p></div>
    <div class="edi-if-cell edi-if-cell--fork-arm-no">
        <div class="edi-vi-fork-arm edi-vi-fork-arm--no">
            <span class="edi-vi-tag">{no_label}</span>
            <div class="edi-vi-pill edi-vi-pill--err">{no_pill}</div>
            <div class="edi-vi-terminus"><span class="edi-vi-terminus-bar" aria-hidden="true"></span><span class="edi-vi-terminus-lbl">End</span></div>
        </div>
    </div>
    <div class="edi-if-cell edi-if-cell--fork-arm-yes">
        <div class="edi-vi-fork-arm edi-vi-fork-arm--yes">
            <span class="edi-vi-tag">{yes_label}</span>
            <div class="edi-vi-pill edi-vi-pill--ok">{yes_pill}</div>
            <div class="edi-vi-terminus edi-vi-terminus--continue"><span class="edi-vi-terminus-bar" aria-hidden="true"></span><span class="edi-vi-terminus-lbl">Next</span></div>
        </div>
    </div>
    <div class="edi-if-cell edi-if-cell--fork-note-yes"><p class="edi-if-fork-note">{yes_note}</p></div>
</div>"""


def fork_continue(no_label: str, no_pill: str, yes_label: str, yes_pill: str, no_note: str, yes_note: str) -> str:
    """Fork where No stops this branch but Yes continues (use line-drop style on No)."""
    return f"""
<div class="edi-if-row edi-if-row--fork-split edi-poc-fork">
    <div class="edi-if-cell edi-if-cell--fork-note-no"><p class="edi-if-fork-note">{no_note}</p></div>
    <div class="edi-if-cell edi-if-cell--fork-arm-no">
        <div class="edi-vi-fork-arm edi-vi-fork-arm--no">
            <span class="edi-vi-tag">{no_label}</span>
            <div class="edi-vi-pill edi-vi-pill--warn">{no_pill}</div>
            <div class="edi-vi-terminus edi-vi-terminus--continue"><span class="edi-vi-terminus-bar" aria-hidden="true"></span><span class="edi-vi-terminus-lbl">Next line</span></div>
        </div>
    </div>
    <div class="edi-if-cell edi-if-cell--fork-arm-yes">
        <div class="edi-vi-fork-arm edi-vi-fork-arm--yes">
            <span class="edi-vi-tag">{yes_label}</span>
            <div class="edi-vi-pill edi-vi-pill--ok">{yes_pill}</div>
            <div class="edi-vi-terminus edi-vi-terminus--continue"><span class="edi-vi-terminus-bar" aria-hidden="true"></span><span class="edi-vi-terminus-lbl">Next</span></div>
        </div>
    </div>
    <div class="edi-if-cell edi-if-cell--fork-note-yes"><p class="edi-if-fork-note">{yes_note}</p></div>
</div>"""


def build_flow(lang: str) -> str:
    en = lang == "en"
    cap = "Flow + key points" if en else "Flujo + puntos clave"
    parts: list[str] = []

    def L(en_s: str, es_s: str) -> str:
        return en_s if en else es_s

    parts.append(layer_band(L("Ingestion layer", "Capa de ingesta")))
    parts.append(
        bre_step(
            "1",
            L("BEES Sync Service", "BEES Sync Service"),
            L("Broker EDI → canonical JSON", "Broker EDI → JSON canónico"),
            "",
            L("Sync intake", "Ingesta Sync"),
            L("HTTP POST from broker; extract and normalize to canonical <code>order</code> JSON.", "POST HTTP del broker; extraer y normalizar al JSON canónico <code>order</code>."),
            False,
            node_class="edi-vi-node--sync",
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(
            L("Level 1<br>OK?", "¿Nivel 1<br>OK?"),
            L("Format gate", "Compuerta de formato"),
            L("Schema / required fields at Sync — reject before BRE.", "Esquema / campos obligatorios en Sync — rechazo antes del BRE."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected at Sync<br>· HTTP · stop", "Rechazado en Sync<br>· HTTP · fin"),
            "Yes" if en else "Sí",
            L("Forward to Link BRE", "Pasar a Link BRE"),
            L("<strong>No:</strong> synchronous rejection; no BRE handoff.", "<strong>No:</strong> rechazo síncrono; sin handoff al BRE."),
            L("<strong>Yes:</strong> continue to Link BRE validation.", "<strong>Sí:</strong> continuar a validación Link BRE."),
        )
    )
    parts.append(arrow())
    parts.append(
        bre_step(
            "2",
            L("Link BRE receives order", "Link BRE recibe pedido"),
            L("Canonical payload + trace", "Payload canónico + traza"),
            "",
            L("BRE entry", "Entrada BRE"),
            L("<code>requestTraceId</code>, country, vendor context attached for all downstream calls.", "<code>requestTraceId</code>, país y vendor para todas las llamadas posteriores."),
            True,
        )
    )

    parts.append(layer_band(L("Validation · 1st layer (order-level)", "Validación · 1ª capa (nivel pedido)")))

    # POC
    parts.append(arrow())
    parts.append(
        bre_step(
            "3",
            L("POC matching", "POC matching"),
            L("1st layer rule", "Regla 1ª capa"),
            "",
            L("Rule intent", "Intención"),
            L("Resolve <code>VendorAccountID</code> for country + vendor.", "Resolver <code>VendorAccountID</code> para país + vendor."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("Accounts Service", "Accounts Service"),
            L("Account / GLN lookup", "Lookup cuenta / GLN"),
            "edi-vi-node--accounts",
            L("GET · lookup", "GET · lookup"),
            L("Communication", "Comunicación"),
            L("BRE → Accounts: direct <code>AccountID</code>, else GLN (Mod-10) or RFC+SUC.", "BRE → Accounts: <code>AccountID</code> directo, si no GLN (Mod-10) o RFC+SUC."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(
            L("POC<br>resolved?", "¿POC<br>resuelto?"),
            L("Outcome", "Resultado"),
            L("No → <strong>Blocked</strong> (hold for account fix). Yes → substitute IDs and continue.", "No → <strong>Bloqueado</strong>. Sí → sustituir IDs y continuar."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Blocked · POC", "Bloqueado · POC"),
            "Yes" if en else "Sí",
            L("Continue", "Continuar"),
            L("<strong>No:</strong> stop order-level path; ops queue.", "<strong>No:</strong> detiene ruta a nivel pedido; cola ops."),
            L("<strong>Yes:</strong> next order-level rule.", "<strong>Sí:</strong> siguiente regla a nivel pedido."),
        )
    )

    # PO uniqueness
    parts.append(arrow())
    parts.append(
        bre_step(
            "4",
            L("PO uniqueness", "Unicidad PO"),
            L("1st layer rule", "Regla 1ª capa"),
            "",
            L("Rule intent", "Intención"),
            L("Build key: <code>poNumber</code> + <code>VendorAccountID</code> + delivery date.", "Clave: <code>poNumber</code> + <code>VendorAccountID</code> + fecha entrega."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("Orders", "Orders"),
            L("Duplicate PO query", "Consulta PO duplicado"),
            "edi-vi-node--orders",
            L("GET · search", "GET · búsqueda"),
            L("Communication", "Comunicación"),
            L("BRE → Orders base: same POC + PO + delivery date already exists?", "BRE → base Orders: ¿mismo POC + PO + fecha?"),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("PO unique?", "¿PO único?"), L("Outcome", "Resultado"), L("No → <strong>Blocked</strong> (duplicate). Yes → continue.", "No → <strong>Bloqueado</strong>. Sí → continuar."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Blocked · duplicate PO", "Bloqueado · PO dup"),
            "Yes" if en else "Sí",
            L("Continue", "Continuar"),
            L("<strong>No:</strong> hold until retailer confirms.", "<strong>No:</strong> hold hasta confirmación."),
            L("<strong>Yes:</strong> delivery rules.", "<strong>Sí:</strong> reglas de entrega."),
        )
    )

    # Delivery range
    parts.append(arrow())
    parts.append(
        bre_step(
            "5",
            L("Delivery range", "Rango de entrega"),
            L("1st layer rule", "Regla 1ª capa"),
            "",
            L("Rule intent", "Intención"),
            L("Validate requested date against allowed calendar range.", "Validar fecha solicitada contra rango permitido."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("BRE engine", "Motor BRE"),
            L("Delivery range config", "Config rango entrega"),
            "edi-vi-node--bre",
            L("READ · rules", "READ · reglas"),
            L("Communication", "Comunicación"),
            L("BRE → engine: load range / frequency policy for country + vendor.", "BRE → motor: política de rango / frecuencia por país + vendor."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("In range?", "¿En rango?"), L("Outcome", "Resultado"), L("No → <strong>Rejected</strong>. Yes → delivery window.", "No → <strong>Rechazado</strong>. Sí → ventana de entrega."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected · range", "Rechazado · rango"),
            "Yes" if en else "Sí",
            L("Continue", "Continuar"),
            L("<strong>No:</strong> terminate order.", "<strong>No:</strong> termina pedido."),
            L("<strong>Yes:</strong> cart window check.", "<strong>Sí:</strong> chequeo ventana Cart."),
        )
    )

    # Delivery window
    parts.append(arrow())
    parts.append(
        bre_step(
            "6",
            L("Delivery window", "Ventana de entrega"),
            L("1st layer rule", "Regla 1ª capa"),
            "",
            L("Rule intent", "Intención"),
            L("Match delivery date to POC delivery frequency / window.", "Alinear fecha con frecuencia / ventana del POC."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("Cart", "Cart"),
            L("Delivery window API", "API ventana entrega"),
            "edi-vi-node--cart",
            L("POST · validate", "POST · validar"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: frequency / valid delivery window for POC.", "BRE → Cart: frecuencia / ventana válida para el POC."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("Window OK?", "¿Ventana OK?"), L("Outcome", "Resultado"), L("No → <strong>Rejected</strong>. Yes → DC validation.", "No → <strong>Rechazado</strong>. Sí → validación DC."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected · window", "Rechazado · ventana"),
            "Yes" if en else "Sí",
            L("Continue", "Continuar"),
            L("<strong>No:</strong> invalid delivery window.", "<strong>No:</strong> ventana inválida."),
            L("<strong>Yes:</strong> DC gate.", "<strong>Sí:</strong> compuerta DC."),
        )
    )

    # DC validation
    parts.append(arrow())
    parts.append(
        bre_step(
            "7",
            L("DC validation", "Validación DC"),
            L("1st layer rule", "Regla 1ª capa"),
            "",
            L("Rule intent", "Intención"),
            L("Read <code>deliveryCenterId</code> from account; Flow 1 vs Flow 2.", "Leer <code>deliveryCenterId</code> de cuenta; Flujo 1 vs 2."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("Accounts Service", "Accounts Service"),
            L("DC on account", "DC en cuenta"),
            "edi-vi-node--accounts",
            L("GET · account", "GET · cuenta"),
            L("Communication", "Comunicación"),
            L("BRE → Accounts: fetch <code>deliveryCenterId</code> (not from EDI payload).", "BRE → Accounts: obtener <code>deliveryCenterId</code> (no del payload EDI)."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("DC valid?", "¿DC válido?"), L("Outcome", "Resultado"), L("Missing DC → <strong>Blocked</strong>. Valid → route billing flow.", "DC ausente → <strong>Bloqueado</strong>. Válido → flujo facturación."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Blocked · DC", "Bloqueado · DC"),
            "Yes" if en else "Sí",
            L("Line-level phase", "Fase línea"),
            L("<strong>No:</strong> hold for BU DC assignment.", "<strong>No:</strong> hold hasta asignación DC."),
            L("<strong>Yes:</strong> start 2nd layer (per line).", "<strong>Sí:</strong> iniciar 2ª capa (por línea)."),
        )
    )

    parts.append(layer_band(L("Validation · 2nd layer (line-level)", "Validación · 2ª capa (nivel línea)")))
    parts.append(arrow())
    parts.append(
        bre_step(
            "8",
            L("For each line item", "Por cada línea"),
            L("2nd layer loop", "Bucle 2ª capa"),
            "",
            L("Scope", "Alcance"),
            L("Run line gates in sequence; partial accept when lines drop.", "Ejecutar compuertas en secuencia; aceptación parcial si caen líneas."),
            False,
        )
    )

    # UPC
    parts.append(arrow())
    parts.append(
        bre_step("9", L("UPC matching", "UPC matching"), L("2nd layer rule", "Regla 2ª capa"), "", L("Per line", "Por línea"), L("Map GTIN/UPC to catalog SKU.", "Mapear GTIN/UPC a SKU catálogo."), True)
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("Items &amp; Catalog", "Items &amp; Catalog"),
            L("SKU resolution", "Resolución SKU"),
            "edi-vi-node--catalog",
            L("GET · catalog", "GET · catálogo"),
            L("Communication", "Comunicación"),
            L("BRE → Catalog (+ POC mapping / PO Reader when configured).", "BRE → Catálogo (+ mapeo POC / PO Reader si aplica)."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("UPC match?", "¿UPC OK?"), L("Outcome", "Resultado"), L("No → line <strong>Blocked</strong>. Yes → package.", "No → línea <strong>Bloqueada</strong>. Sí → paquete."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Blocked · line UPC", "Bloqueado · UPC"),
            "Yes" if en else "Sí",
            L("Package rule", "Regla paquete"),
            L("<strong>No:</strong> hold line.", "<strong>No:</strong> hold línea."),
            L("<strong>Yes:</strong> package validation.", "<strong>Sí:</strong> validación paquete."),
        )
    )

    # Package
    parts.append(arrow())
    parts.append(
        bre_step(
            "10",
            L("Package validation", "Validación paquete"),
            L("2nd layer rule · EDI BRE", "Regla 2ª capa · EDI BRE"),
            "",
            L("Internal", "Interno"),
            L("BRE applies <code>pack_conversion_factor</code> / commercial params (no external HTTP in MVP path).", "BRE aplica <code>pack_conversion_factor</code> / params comerciales."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("Package OK?", "¿Paquete OK?"), L("Outcome", "Resultado"), L("No → <strong>Rejected</strong> (whole order). Yes → stock.", "No → <strong>Rechazado</strong> (pedido). Sí → stock."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected · package", "Rechazado · paquete"),
            "Yes" if en else "Sí",
            L("Stock check", "Chequeo stock"),
            L("<strong>No:</strong> invalid conversion.", "<strong>No:</strong> conversión inválida."),
            L("<strong>Yes:</strong> stock availability.", "<strong>Sí:</strong> disponibilidad stock."),
        )
    )

    # Stock
    parts.append(arrow())
    parts.append(bre_step("11", L("Stock availability", "Disponibilidad stock"), L("2nd layer rule", "Regla 2ª capa"), "", L("Per line", "Por línea"), L("Cart stock signal for SKU/qty.", "Señal de stock Cart para SKU/cant."), True))
    parts.append(arrow())
    parts.append(
        service_step(
            L("Cart", "Cart"),
            L("Stock validation", "Validación stock"),
            "edi-vi-node--cart",
            L("POST · stock", "POST · stock"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: available quantity for line.", "BRE → Cart: cantidad disponible por línea."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("In stock?", "¿Hay stock?"), L("Outcome", "Resultado"), L("No → <strong>drop line</strong> (partial accept path). Yes → tax.", "No → <strong>descartar línea</strong>. Sí → impuestos."), True)
    )
    parts.append(arrow())
    parts.append(
        fork_continue(
            "No",
            L("Drop line · stock", "Descartar línea"),
            "Yes" if en else "Sí",
            L("Keep line", "Mantener línea"),
            L("<strong>No:</strong> reject only this SKU; continue order.", "<strong>No:</strong> rechaza solo SKU; sigue pedido."),
            L("<strong>Yes:</strong> tax validation.", "<strong>Sí:</strong> validación impuestos."),
        )
    )

    # Tax
    parts.append(arrow())
    parts.append(bre_step("12", L("Tax validation", "Validación impuestos"), L("2nd layer rule", "Regla 2ª capa"), "", L("Per line", "Por línea"), L("Compare line tax vs reference.", "Comparar impuesto línea vs referencia."), True))
    parts.append(arrow())
    parts.append(
        service_step(
            L("Price MS", "Price MS"),
            L("Tax reference", "Referencia impuestos"),
            "edi-vi-node--pricem",
            L("GET · pricing", "GET · precios"),
            L("Communication", "Comunicación"),
            L("BRE → Price MS: expected tax components per SKU/POC.", "BRE → Price MS: componentes de impuesto esperados."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("Tax OK?", "¿Impuesto OK?"), L("Outcome", "Resultado"), L("No → <strong>Blocked</strong> (price hold path). Yes → price.", "No → <strong>Bloqueado</strong>. Sí → precio."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Blocked · tax", "Bloqueado · impuesto"),
            "Yes" if en else "Sí",
            L("Price rule", "Regla precio"),
            L("<strong>No:</strong> hold for price alignment.", "<strong>No:</strong> hold alineación precio."),
            L("<strong>Yes:</strong> price validation.", "<strong>Sí:</strong> validación precio."),
        )
    )

    # Price
    parts.append(arrow())
    parts.append(bre_step("13", L("Price validation", "Validación precio"), L("2nd layer rule", "Regla 2ª capa"), "", L("Per line", "Por línea"), L("Tolerance vs BEES reference price.", "Tolerancia vs precio referencia BEES."), True))
    parts.append(arrow())
    parts.append(
        service_step(
            L("Price MS", "Price MS"),
            L("Price reference", "Referencia precio"),
            "edi-vi-node--pricem",
            L("GET · price", "GET · precio"),
            L("Communication", "Comunicación"),
            L("BRE → Price MS: reference unit price + tolerance band.", "BRE → Price MS: precio unitario + banda tolerancia."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("Price OK?", "¿Precio OK?"), L("Outcome", "Resultado"), L("No → <strong>Blocked</strong> until D-1. Yes → next line or aggregate.", "No → <strong>Bloqueado</strong> hasta D-1. Sí → agregado."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Blocked · price", "Bloqueado · precio"),
            "Yes" if en else "Sí",
            L("Next line / aggregate", "Sig. línea / agregado"),
            L("<strong>No:</strong> discrepancy hold.", "<strong>No:</strong> hold discrepancia."),
            L("<strong>Yes:</strong> more lines or stage 3.", "<strong>Sí:</strong> más líneas o etapa 3."),
        )
    )

    parts.append(arrow())
    parts.append(
        diamond(
            L("Any lines<br>left?", "¿Quedan<br>líneas?"),
            L("Line aggregate", "Agregado líneas"),
            L("Zero lines → <strong>Rejected</strong>. ≥1 → 3rd layer.", "Cero líneas → <strong>Rechazado</strong>. ≥1 → 3ª capa."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected · no lines", "Rechazado · sin líneas"),
            "Yes" if en else "Sí",
            L("3rd layer", "3ª capa"),
            L("<strong>No:</strong> nothing to fulfill.", "<strong>No:</strong> nada que cumplir."),
            L("<strong>Yes:</strong> MOQ / MAX.", "<strong>Sí:</strong> MOQ / MAX."),
        )
    )

    parts.append(layer_band(L("Validation · 3rd layer (order aggregate)", "Validación · 3ª capa (agregado pedido)")))

    # MOQ
    parts.append(arrow())
    parts.append(bre_step("14", L("Minimum order qty", "Cantidad mínima pedido"), L("3rd layer rule", "Regla 3ª capa"), "", L("Order aggregate", "Agregado"), L("MOQ on validated cart.", "MOQ sobre carrito validado."), False))
    parts.append(arrow())
    parts.append(
        service_step(
            L("Cart", "Cart"),
            L("MOQ validation", "Validación MOQ"),
            "edi-vi-node--cart",
            L("POST · MOQ", "POST · MOQ"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: minimum quantity for POC / order.", "BRE → Cart: cantidad mínima para POC / pedido."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("MOQ met?", "¿Cumple MOQ?"), L("Outcome", "Resultado"), L("No → <strong>Rejected</strong>. Yes → MAX.", "No → <strong>Rechazado</strong>. Sí → MAX."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected · MOQ", "Rechazado · MOQ"),
            "Yes" if en else "Sí",
            L("MAX rule", "Regla MAX"),
            L("<strong>No:</strong> below minimum.", "<strong>No:</strong> bajo mínimo."),
            L("<strong>Yes:</strong> maximum check.", "<strong>Sí:</strong> chequeo máximo."),
        )
    )

    # MAX
    parts.append(arrow())
    parts.append(bre_step("15", L("Maximum order qty", "Cantidad máxima pedido"), L("3rd layer rule", "Regla 3ª capa"), "", L("Order aggregate", "Agregado"), L("MAX on validated cart.", "MAX sobre carrito validado."), False))
    parts.append(arrow())
    parts.append(
        service_step(
            L("Cart", "Cart"),
            L("MAX validation", "Validación MAX"),
            "edi-vi-node--cart",
            L("POST · MAX", "POST · MAX"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: maximum allowed quantity.", "BRE → Cart: cantidad máxima permitida."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        diamond(L("Within MAX?", "¿Dentro MAX?"), L("Outcome", "Resultado"), L("No → <strong>Rejected</strong>. Yes → create order.", "No → <strong>Rechazado</strong>. Sí → crear pedido."), True)
    )
    parts.append(arrow())
    parts.append(
        fork(
            "No",
            L("Rejected · MAX", "Rechazado · MAX"),
            "Yes" if en else "Sí",
            L("Order creation", "Creación pedido"),
            L("<strong>No:</strong> above maximum.", "<strong>No:</strong> sobre máximo."),
            L("<strong>Yes:</strong> persist order in BEES.", "<strong>Sí:</strong> persistir pedido en BEES."),
        )
    )

    parts.append(arrow())
    parts.append(
        bre_step(
            "16",
            L("Order creation", "Creación del pedido"),
            L("3rd layer · BEES OMS path", "3ª capa · ruta OMS BEES"),
            "",
            L("Persist", "Persistir"),
            L("Emit <code>order_continued</code> with line counts; set aggregate status.", "Emitir <code>order_continued</code> con conteo de líneas; estado agregado."),
            False,
        )
    )

    parts.append(layer_band(L("Handoff layer", "Capa de handoff")))
    parts.append(arrow())
    parts.append(
        bre_step(
            "17",
            L("Status routing", "Enrutado de estado"),
            L("Accepted · Partial · Rejected · Pending", "Aceptado · Parcial · Rechazado · Pendiente"),
            "",
            L("Outcomes", "Resultados"),
            L("<strong>Accepted</strong> full ingestion · <strong>Partial</strong> line subset · <strong>Rejected</strong> full reject · <strong>Pending</strong> processing/hold.", "<strong>Aceptado</strong> ingesta total · <strong>Parcial</strong> · <strong>Rechazado</strong> · <strong>Pendiente</strong>."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("OMS", "OMS"),
            L("Order handoff", "Handoff pedido"),
            "edi-vi-node--oms",
            L("POST · order", "POST · pedido"),
            L("Communication", "Comunicación"),
            L("BRE → OMS: accepted / partially accepted orders for BU ERP pipeline.", "BRE → OMS: pedidos aceptados / parciales hacia ERP BU."),
            False,
        )
    )
    parts.append(arrow())
    parts.append(
        service_step(
            L("Central Tracking", "Central Tracking"),
            L("Index + events", "Índice + eventos"),
            "edi-vi-node--tracking",
            L("POST · index", "POST · índice"),
            L("Communication", "Comunicación"),
            L("BRE → Central Tracking: structured rule outcomes for retailer + vendor ops.", "BRE → Central Tracking: resultados estructurados para retailer y ops."),
            True,
        )
    )
    parts.append(arrow())
    parts.append(
        f'<div class="edi-if-row edi-if-row--note-right"><div class="edi-if-cell edi-if-cell--graph">'
        f'<div class="edi-vi-terminus"><span class="edi-vi-terminus-bar" aria-hidden="true"></span>'
        f'<span class="edi-vi-terminus-lbl">{"End" if en else "Fin"}</span></div></div>'
        f'<div class="edi-if-cell edi-if-cell--note-side"><strong class="edi-if-ls-title">{"Traceability" if en else "Trazabilidad"}</strong>'
        f'<p class="edi-if-ls-desc">{"Events across Sync → BRE → services → OMS → Central Tracking." if en else "Eventos en Sync → BRE → servicios → OMS → Central Tracking."}</p></div></div>'
    )

    legend_en = """
<div class="edi-vi-sk-item"><span class="edi-vi-sk-bre"></span> Link BRE</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-accounts"></span> Accounts / Orders</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-cart"></span> Cart</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-catalog"></span> Catalog</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-pricem"></span> Price MS</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-shape edi-vi-sk-step"></span> Step</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-shape edi-vi-sk-diamond"></span> Decision</div>
<div class="edi-vi-sk-item"><span class="edi-vi-sk-shape edi-vi-sk-err"></span> Error</div>"""

    legend_es = legend_en  # same labels for service names

    title_en = "EDI BRE — end-to-end solution flow (step-by-step)"
    title_es = "EDI BRE — flujo extremo a extremo (paso a paso)"
    heading_id_en = "e2e-journey-flow-heading"
    heading_id_es = "e2e-journey-flow-heading-es"

    title = title_en if en else title_es
    heading_id = heading_id_en if en else heading_id_es
    legend = legend_en if en else legend_es

    body = "\n".join(parts)
    return f"""
<div class="edi-integ-flow edi-integ-flow--e2e-detailed" role="region" aria-labelledby="{heading_id}">
    <div class="edi-integ-flow-title" id="{heading_id}">{title}</div>
    <div class="edi-integ-flow-body">
        <div class="edi-if-visual">
            <div class="edi-if-visual-head">
                <span class="edi-if-visual-caption">{cap}</span>
                <div class="edi-vi-shape-key edi-vi-shape-key--wide" aria-hidden="true">{legend}</div>
            </div>
            <div class="edi-if-flow-track edi-if-flow-track--e2e">
{body}
            </div>
        </div>
    </div>
</div>"""


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    en_block = build_flow("en")
    es_block = build_flow("es")

    if MARKER_EN_START not in html or MARKER_ES_START not in html:
        raise SystemExit("Markers not found in index.html — add E2E_JOURNEY_FLOW_*_START/END")

    html = re.sub(
        rf"{MARKER_EN_START}.*?{MARKER_EN_END}",
        f"{MARKER_EN_START}\n{en_block}\n{MARKER_EN_END}",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        rf"{MARKER_ES_START}.*?{MARKER_ES_END}",
        f"{MARKER_ES_START}\n{es_block}\n{MARKER_ES_END}",
        html,
        count=1,
        flags=re.DOTALL,
    )
    INDEX.write_text(html, encoding="utf-8")
    print("Updated", INDEX)


if __name__ == "__main__":
    main()
