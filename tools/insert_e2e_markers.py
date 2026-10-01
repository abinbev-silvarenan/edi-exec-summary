import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'<div class="edi-integ-flow" role="region" aria-labelledby="e2e-journey-flow-heading">.*?</div>\s*</div>\s*</div>\s*</div>\s*\n\n<div class="table-scroll">',
    "<!-- E2E_JOURNEY_FLOW_EN_START -->\n<!-- E2E_JOURNEY_FLOW_EN_END -->\n\n<div class=\"table-scroll\">",
    t,
    count=1,
    flags=re.DOTALL,
)
t = re.sub(
    r'<div class="edi-integ-flow" role="region" aria-labelledby="e2e-journey-flow-heading-es">.*?</div>\s*</div>\s*</div>\s*</div>\s*\n\n<table>',
    "<!-- E2E_JOURNEY_FLOW_ES_START -->\n<!-- E2E_JOURNEY_FLOW_ES_END -->\n\n<table>",
    t,
    count=1,
    flags=re.DOTALL,
)
p.write_text(t, encoding="utf-8")
print("done", "E2E_JOURNEY_FLOW_EN_START" in t)
