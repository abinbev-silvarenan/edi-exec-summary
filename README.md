# EDI Order Validation — Executive Summary

Self-contained HTML executive summary for the **BEES Link BRE — EDI Order Validation** initiative (English & Spanish, single file, no external dependencies).

## Files

| File | Purpose |
| --- | --- |
| `index.html` | GitHub Pages entry point (latest version). |
| `EDI-Order-Validation-Scope_Exec_Summary-v1.1.html` | Versioned copy of the same document. |
| `.nojekyll` | Tells GitHub Pages to skip Jekyll processing and serve files as-is. |

## View it online

Once GitHub Pages is enabled for this repo, the latest version will be available at:

```
https://silarerenan-cmyk.github.io/edi-bre-exec-summary/
```

## Enable GitHub Pages (one-time)

1. Open this repo on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**:
   - **Source:** Deploy from a branch.
   - **Branch:** `main` / `/ (root)`.
4. Save. The page should be live in 1–2 minutes at the URL above.

## Updating the document

Replace `index.html` (and, optionally, bump the versioned file name) and push to `main`. GitHub Pages will publish the new version automatically.

## Contents

The document covers, in both EN and ES:

- Executive summary, scope, audience, and timeline.
- End-to-end BRE solution flow (3 validation layers, with **Blocked** vs **Rejected** outcomes per business rule).
- Technical requirements for each business rule (Order Integration, Match POC, PO Uniqueness, Delivery Dates, UPC Matching, Package, SKU Availability, Price Validation, Min/Max Order Quantity).
- Canonical JSON contract (v1.24.0) — schema, payload examples, field-by-field reference.
- "What we count on the BU for" dependencies per rule.
- References to the underlying Confluence HLRs (BLK space).
