#!/usr/bin/env python3
"""Generate edi-integ-flow diagrams for T9–T13 (EN + ES) into index.html markers."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

_spec = importlib.util.spec_from_file_location(
    "e2e_gen", Path(__file__).parent / "generate_e2e_journey_flow.py"
)
e2e = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e2e)  # type: ignore

arrow = e2e.arrow
bre_step = e2e.bre_step
service_step = e2e.service_step
diamond = e2e.diamond
fork = e2e.fork
fork_continue = e2e.fork_continue


def wrap_flow(flow_id: str, title: str, caption: str, body: str) -> str:
    diagram_id = f"{flow_id}-diagram"
    return f"""
<div class="edi-integ-flow edi-integ-flow--e2e-detailed" role="region" aria-labelledby="{diagram_id}">
    <div class="edi-integ-flow-title" id="{diagram_id}">{title}</div>
    <div class="edi-integ-flow-body">
        <div class="edi-if-visual">
            <div class="edi-if-visual-head">
                <span class="edi-if-visual-caption">{caption}</span>
                <div class="edi-vi-shape-key" aria-hidden="true">
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-bre"></span> Link BRE</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-accounts"></span> Accounts</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-cart"></span> Cart</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-catalog"></span> Catalog / chain</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-pricem"></span> Price MS</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-shape edi-vi-sk-step"></span> Step</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-shape edi-vi-sk-diamond"></span> Decision</div>
                    <div class="edi-vi-sk-item"><span class="edi-vi-sk-shape edi-vi-sk-err"></span> Error</div>
                </div>
            </div>
            <div class="edi-if-flow-track edi-if-flow-track--e2e">
{body}
            </div>
        </div>
    </div>
</div>"""


def make_L(lang: str):
    def L(en: str, es: str) -> str:
        return en if lang == "en" else es

    return L


def build_t9(lang: str) -> str:
    L = make_L(lang)
    parts = [
        bre_step(
            "1",
            L("DC validation", "Validación DC"),
            L("Gate 2c · after POC", "Compuerta 2c · tras POC"),
            "",
            L("Rule intent", "Intención"),
            L("Select Flow 1 (direct) vs Flow 2 (remote billing FR subset).", "Elegir Flujo 1 (directo) vs Flujo 2 (subconjunto FR)."),
            False,
        ),
        arrow(),
        diamond(
            L("Toggle<br>on?", "¿Toggle<br>activo?"),
            L("Configuration", "Configuración"),
            L("Off → skip DC lookup; default Flow 1 for all orders.", "Off → omitir lookup DC; Flujo 1 por defecto."),
            True,
        ),
        arrow(),
        fork(
            "No",
            L("Flow 1 · skip DC", "Flujo 1 · sin DC"),
            "Yes" if lang == "en" else "Sí",
            L("Lookup DC", "Lookup DC"),
            L("<strong>Off:</strong> no pass/fail on DC.", "<strong>Off:</strong> sin pass/fail en DC."),
            L("<strong>On:</strong> read account DC.", "<strong>On:</strong> leer DC de cuenta."),
        ),
        arrow(),
        service_step(
            L("Accounts Service", "Accounts Service"),
            L("Read <code>deliveryCenterId</code>", "Leer <code>deliveryCenterId</code>"),
            "edi-vi-node--accounts",
            L("GET · account", "GET · cuenta"),
            L("Communication", "Comunicación"),
            L("BRE → Accounts: POC–vendor contract field (not EDI payload).", "BRE → Accounts: campo en contrato POC–vendor (no payload EDI)."),
            False,
        ),
        arrow(),
        diamond(
            L("DC<br>present?", "¿DC<br>presente?"),
            L("Outcome", "Resultado"),
            L("Missing → <strong>Blocked</strong> <code>missing_dc_assignment</code>.", "Ausente → <strong>Bloqueado</strong> <code>missing_dc_assignment</code>."),
            True,
        ),
        arrow(),
        fork(
            "No",
            L("Blocked · DC", "Bloqueado · DC"),
            "Yes" if lang == "en" else "Sí",
            L("Route flow", "Enrutar flujo"),
            L("<strong>No:</strong> hold for BU DC fix.", "<strong>No:</strong> hold hasta corrección BU."),
            L("<strong>Yes:</strong> compare remote DC list.", "<strong>Sí:</strong> comparar lista DC remoto."),
        ),
        arrow(),
        bre_step(
            "2",
            L("Flow routing", "Enrutado de flujo"),
            L("Remote DC list vs <code>deliveryCenterId</code>", "Lista DC remoto vs <code>deliveryCenterId</code>"),
            "",
            L("BRE engine", "Motor BRE"),
            L("Flow 2 → FR rules only + <code>skipped — remote billing</code> logs.", "Flujo 2 → solo reglas FR + logs <code>skipped — remote billing</code>."),
            True,
        ),
        arrow(),
        diamond(L("Remote<br>DC?", "¿DC<br>remoto?"), L("Outcome", "Resultado"), L("Yes → Flow 2 (e.g. AR DC 60). No → Flow 1 full rule set.", "Sí → Flujo 2 (ej. AR DC 60). No → Flujo 1 completo."), False),
        arrow(),
        fork(
            "Yes" if lang == "en" else "Sí",
            L("Flow 2 · FR subset", "Flujo 2 · subconjunto FR"),
            "No",
            L("Flow 1 · full set", "Flujo 1 · set completo"),
            L("<strong>Remote:</strong> UPC, price, DC per config.", "<strong>Remoto:</strong> UPC, precio, DC según config."),
            L("<strong>Direct:</strong> all toggled rules.", "<strong>Directo:</strong> todas las reglas activas."),
        ),
    ]
    title = L("DC validation — Link BRE → Accounts", "Validación DC — Link BRE → Accounts")
    fid = "section-tech-dc-flow" if lang == "en" else "section-tech-dc-flow-es"
    cap = L("Flow + key points", "Flujo + puntos clave")
    return wrap_flow(fid, title, cap, "\n".join(parts))


def build_t10(lang: str) -> str:
    L = make_L(lang)
    parts = [
        bre_step(
            "1",
            L("Package validation", "Validación de paquete"),
            L("Per line · after UPC", "Por línea · tras UPC"),
            "",
            L("Rule intent", "Intención"),
            L("Convert retailer qty to ABI billing boxes via <code>pack_conversion_factor</code>.", "Convertir cantidad minorista a cajas ABI vía <code>pack_conversion_factor</code>."),
            False,
        ),
        arrow(),
        service_step(
            L("Chain / commercial params", "Params comerciales / cadena"),
            L("Resolve <code>zoneChainId</code> + factor", "Resolver <code>zoneChainId</code> + factor"),
            "edi-vi-node--catalog",
            L("GET · EDI_SKU_COMMERCIAL_PARAMS", "GET · EDI_SKU_COMMERCIAL_PARAMS"),
            L("Communication", "Comunicación"),
            L("BRE → chain scope + active conversion factor for SKU + zone.", "BRE → alcance cadena + factor activo para SKU + zona."),
            True,
        ),
        arrow(),
        bre_step(
            "2",
            L("Compute boxes", "Calcular cajas"),
            L("<code>qty ÷ pack_conversion_factor</code>", "<code>qty ÷ pack_conversion_factor</code>"),
            "",
            L("EDI BRE", "EDI BRE"),
            L("Optional cross-check of retailer-declared pack factor.", "Chequeo opcional del factor declarado por minorista."),
            False,
        ),
        arrow(),
        diamond(
            L("Integer<br>boxes?", "¿Cajas<br>enteras?"),
            L("Outcome", "Resultado"),
            L("Fail → <strong>reject entire order</strong> <code>order_rejected_invalid_package</code>.", "Fallo → <strong>rechazar pedido completo</strong>."),
            True,
        ),
        arrow(),
        fork(
            "No",
            L("Rejected · package", "Rechazado · paquete"),
            "Yes" if lang == "en" else "Sí",
            L("Rewrite line qty", "Reescribir qty línea"),
            L("<strong>No:</strong> no partial accept.", "<strong>No:</strong> sin aceptación parcial."),
            L("<strong>Yes:</strong> persist billing boxes; next line gate.", "<strong>Sí:</strong> persistir cajas; siguiente compuerta."),
        ),
    ]
    fid = "section-tech-package-flow" if lang == "en" else "section-tech-package-flow-es"
    return wrap_flow(
        fid,
        L("Package validation — Link BRE → commercial params", "Validación paquete — Link BRE → params comerciales"),
        L("Flow + key points", "Flujo + puntos clave"),
        "\n".join(parts),
    )


def build_t11(lang: str) -> str:
    L = make_L(lang)
    parts = [
        bre_step(
            "1",
            L("SKU availability", "Disponibilidad SKU"),
            L("Per line · cart-validation", "Por línea · cart-validation"),
            "",
            L("Rule intent", "Intención"),
            L("Delegate stock to same path as app checkout (Stepper <code>PERFORM_CARTS_VALIDATION</code>).", "Delegar stock al mismo path que checkout app."),
            False,
        ),
        arrow(),
        service_step(
            L("Cart", "Cart"),
            L("Stock validation API", "API validación stock"),
            "edi-vi-node--cart",
            L("POST · stock", "POST · stock"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: ATP / availability for SKU + qty at POC.", "BRE → Cart: ATP / disponibilidad para SKU + cant."),
            True,
        ),
        arrow(),
        diamond(
            L("Stock<br>outcome?", "¿Resultado<br>stock?"),
            L("Line outcomes", "Resultados línea"),
            L("Full · partial adjust · zero (drop line).", "Completo · ajuste parcial · cero (descartar línea)."),
            False,
        ),
        arrow(),
        fork_continue(
            "Zero",
            L("Drop line", "Descartar línea"),
            "Partial" if lang == "en" else "Parcial",
            L("Adjust qty", "Ajustar qty"),
            L("<strong>Zero:</strong> remove line; continue order.", "<strong>Cero:</strong> quitar línea; seguir pedido."),
            L("<strong>Partial/Full:</strong> keep or adjust line.", "<strong>Parcial/Completo:</strong> mantener o ajustar línea."),
        ),
        arrow(),
        bre_step(
            "2",
            L("Aggregate lines", "Agregar líneas"),
            L("After all lines", "Tras todas las líneas"),
            "",
            L("Order status", "Estado pedido"),
            L("≥1 line → partial or full accept; 0 lines → reject order.", "≥1 línea → aceptación parcial o total; 0 → rechazo."),
            True,
        ),
    ]
    fid = "section-tech-sku-flow" if lang == "en" else "section-tech-sku-flow-es"
    return wrap_flow(
        fid,
        L("SKU availability — Link BRE → Cart", "Disponibilidad SKU — Link BRE → Cart"),
        L("Flow + key points", "Flujo + puntos clave"),
        "\n".join(parts),
    )


def build_t12(lang: str) -> str:
    L = make_L(lang)
    parts = [
        bre_step(
            "1",
            L("Minimum order qty (MOQ)", "Cantidad mínima (MOQ)"),
            L("3rd layer · order aggregate", "3ª capa · agregado pedido"),
            "",
            L("Prerequisite", "Prerrequisito"),
            L("≥1 line survived Stage 2.", "≥1 línea sobrevivió Etapa 2."),
            False,
        ),
        arrow(),
        service_step(
            L("Cart", "Cart"),
            L("MOQ validation", "Validación MOQ"),
            "edi-vi-node--cart",
            L("POST · MOQ", "POST · MOQ"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: store/vendor MOQ thresholds.", "BRE → Cart: umbrales MOQ por tienda/vendor."),
            True,
        ),
        arrow(),
        diamond(L("MOQ met?", "¿Cumple MOQ?"), L("Outcome", "Resultado"), L("Below MOQ → <strong>reject order</strong>.", "Bajo MOQ → <strong>rechazar pedido</strong>."), False),
        arrow(),
        fork(
            "No",
            L("Rejected · MOQ", "Rechazado · MOQ"),
            "Yes" if lang == "en" else "Sí",
            L("MAX gate", "Compuerta MAX"),
            L("<strong>No:</strong> canonical MOQ reason.", "<strong>No:</strong> razón MOQ canónica."),
            L("<strong>Yes:</strong> continue to MAX.", "<strong>Sí:</strong> continuar a MAX."),
        ),
        arrow(),
        bre_step(
            "2",
            L("Maximum order qty (MAX)", "Cantidad máxima (MAX)"),
            L("3rd layer · order aggregate", "3ª capa · agregado pedido"),
            "",
            L("Rule intent", "Intención"),
            L("MX MVP; skipped T4 / CEDIS channels per HLR.", "MVP MX; omitido T4 / CEDIS según HLR."),
            False,
        ),
        arrow(),
        service_step(
            L("Cart", "Cart"),
            L("MAX validation", "Validación MAX"),
            "edi-vi-node--cart",
            L("POST · MAX", "POST · MAX"),
            L("Communication", "Comunicación"),
            L("BRE → Cart: maximum allowed order quantity.", "BRE → Cart: cantidad máxima permitida."),
            True,
        ),
        arrow(),
        diamond(L("Within MAX?", "¿Dentro MAX?"), L("Outcome", "Resultado"), L("Above MAX → <strong>reject order</strong>.", "Sobre MAX → <strong>rechazar pedido</strong>."), False),
        arrow(),
        fork(
            "No",
            L("Rejected · MAX", "Rechazado · MAX"),
            "Yes" if lang == "en" else "Sí",
            L("Order creation", "Creación pedido"),
            L("<strong>No:</strong> canonical MAX reason.", "<strong>No:</strong> razón MAX canónica."),
            L("<strong>Yes:</strong> proceed to order creation.", "<strong>Sí:</strong> proceder a creación pedido."),
        ),
    ]
    fid = "section-tech-moq-max-flow" if lang == "en" else "section-tech-moq-max-flow-es"
    return wrap_flow(
        fid,
        L("MOQ / MAX — Link BRE → Cart", "MOQ / MAX — Link BRE → Cart"),
        L("Flow + key points", "Flujo + puntos clave"),
        "\n".join(parts),
    )


def build_t13(lang: str) -> str:
    L = make_L(lang)
    parts = [
        bre_step(
            "1",
            L("BRE outcome events", "Eventos de resultado BRE"),
            L("Structured logging", "Logging estructurado"),
            "",
            L("Emit", "Emisión"),
            L("Rule id, outcome, line diagnostics, <code>requestTraceID</code>.", "Id regla, resultado, diagnósticos línea, <code>requestTraceID</code>."),
            False,
        ),
        arrow(),
        service_step(
            L("Central Tracking", "Central Tracking"),
            L("Index order + status", "Indexar pedido + estado"),
            "edi-vi-node--tracking",
            L("POST · index", "POST · índice"),
            L("Communication", "Comunicación"),
            L("BRE → Central Tracking: Accepted / Partial / Rejected / Pending.", "BRE → Central Tracking: Aceptado / Parcial / Rechazado / Pendiente."),
            True,
        ),
        arrow(),
        bre_step(
            "2",
            L("Consumer surfaces", "Superficies consumidoras"),
            L("51859 · 51860 · 57198", "51859 · 51860 · 57198"),
            "",
            L("Paths", "Rutas"),
            L("Retailer read-only · vendor ops reprocess · Phase 2 line resolution.", "Lectura minorista · reproceso ops · Fase 2 líneas."),
            False,
        ),
        arrow(),
        service_step(
            L("OMS", "OMS"),
            L("Accepted orders handoff", "Handoff pedidos aceptados"),
            "edi-vi-node--oms",
            L("POST · order", "POST · pedido"),
            L("Communication", "Comunicación"),
            L("Parallel path: accepted / partial orders to ERP pipeline (not a BRE toggle).", "Ruta paralela: pedidos aceptados/parciales hacia ERP (no es toggle BRE)."),
            True,
        ),
    ]
    fid = "section-tech-central-tracking-flow" if lang == "en" else "section-tech-central-tracking-flow-es"
    return wrap_flow(
        fid,
        L("Central Tracking — BRE events → index → ops / retailer", "Central Tracking — eventos BRE → índice → ops / minorista"),
        L("Flow + key points", "Flujo + puntos clave"),
        "\n".join(parts),
    )


BUILDERS = {
    "T9_EN": lambda: build_t9("en"),
    "T9_ES": lambda: build_t9("es"),
    "T10_EN": lambda: build_t10("en"),
    "T10_ES": lambda: build_t10("es"),
    "T11_EN": lambda: build_t11("en"),
    "T11_ES": lambda: build_t11("es"),
    "T12_EN": lambda: build_t12("en"),
    "T12_ES": lambda: build_t12("es"),
    "T13_EN": lambda: build_t13("en"),
    "T13_ES": lambda: build_t13("es"),
}


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    for key, builder in BUILDERS.items():
        start = f"<!-- RULE_FLOW_{key}_START -->"
        end = f"<!-- RULE_FLOW_{key}_END -->"
        if start not in html:
            raise SystemExit(f"Missing marker {start}")
        block = builder()
        html = re.sub(
            rf"{start}.*?{end}",
            f"{start}\n{block}\n{end}",
            html,
            count=1,
            flags=re.DOTALL,
        )
    INDEX.write_text(html, encoding="utf-8")
    print("Updated rule flows in", INDEX)


if __name__ == "__main__":
    main()
