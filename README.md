# EDI Order Validation — Executive Summary

Self-contained HTML executive summary for the **BEES Link BRE — EDI Order Validation** initiative (English & Spanish, single file). **Typography:** loads **Barlow** and **Work Sans** from Google Fonts (same pairing as the BU business-rules matrix). All other assets are inline.

## Live site

```
https://abinbev-silvarenan.github.io/edi-exec-summary/
```

## GitHub Pages — publish & redeploy

The **Publish site** workflow (`.github/workflows/publish-pages.yml`) copies `index.html` and `.nojekyll` to the **`gh-pages`** branch on every push to `main`.

### One-time setup

1. Open **Settings → Pages** for this repo.
2. Under **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
3. Click **Save**. Wait 2–5 minutes, then open the live URL above.

If Pages is disabled, deploy workflows fail with **404 — ensure GitHub Pages has been enabled** in Settings.

### Redeploy

Push to `main`, or run **Actions → Publish site → Run workflow**. The live site updates after the workflow finishes and Pages propagates (1–2 minutes).

## Files

| File | Purpose |
| --- | --- |
| `index.html` | GitHub Pages entry point (latest version). |
| `EDI-Order-Validation-Scope_Exec_Summary-v1.1.html` | Versioned copy of the same document (regenerate when you cut a new release). |
| `.nojekyll` | Tells GitHub Pages to skip Jekyll processing and serve files as-is. |
| `tools/merge_bu_matrix.mjs` | Re-embeds the BU rules matrix from `../edi-bre-bu-business-rules-matrix.html` into **Technical requirements** (run from repo root if the standalone matrix changes). |

## BU business rules matrix

The **Technical requirements** tab opens with the **Business rules matrix** (BLK-aligned short description / scope / prerequisites). Source of truth for the table HTML lives in the sibling file `edi-bre-bu-business-rules-matrix.html` in the parent folder; after editing it, run:

```bash
node edi-bre-exec-summary/tools/merge_bu_matrix.mjs
```

Then adjust any one-off copy in `index.html` if needed and push to `main`.

## Contents

The document covers, in both EN and ES:

- **Business rules matrix** (first section under Technical requirements): BU scope & prerequisites aligned to BLK HLRs.
- Executive summary, scope, audience, and timeline.
- End-to-end BRE solution flow (3 validation layers, with **Blocked** vs **Rejected** outcomes per business rule).
- Technical requirements for each business rule (Order Integration, Match POC, PO Uniqueness, Delivery Dates, UPC Matching, Package, SKU Availability, Price Validation, Min/Max Order Quantity).
- Canonical JSON contract (v1.24.0) — schema, payload examples, field-by-field reference.
- "What we count on the BU for" dependencies per rule.
- References to the underlying Confluence HLRs (BLK space).
