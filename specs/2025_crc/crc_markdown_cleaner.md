# CRC Markdown Cleaner — Parsing Instructions

Purpose: convert a raw export of a 2025 California Residential Code (CRC) chapter into clean, self-contained markdown suitable for consumption by agentic applications. This document is the canonical set of rules used to produce `ch4.md` in this directory. Apply the same rules to any future chapter.

## 1. Reference files

- **Exemplar output:** `2025_crc/ch4.md` (fully converted Chapter 4, R401–R408).
- **Source:** raw UpCodes export (HTML-to-text with internal links) of the same chapter page. Saved copies live under `C:\Users\kjwil\.local\share\opencode\tool-output\`.
- **IBC-style comparison:** `2024_ibc/ch16_clean.md` — note it uses a _trailing period_ on headings; `ch4.md` does **not**. Always follow the local `2025_crc` style, not the IBC style.

## 2. Source format characteristics (UpCodes export)

- Headings appear as `### [Section RXXX Title](/viewer/california/ca-residential-code-2025/chapter/4/foundations#RXXX)` or `### [RXXX.X Title](...same anchor...#RXXX.X)`.
- Defined terms are inline links: `[drain](/viewer/california/ca-residential-code-2025/chapter/2/definitions#drain_)`. The link text is the plain term; the target is a definition anchor.
- Cross references are inline links: `[Table R401.4.1(2)](#table_R401.4.1-2)` or `[Section R406.2](#R406.2)`.
- Page-chrome lines that must be dropped: `UpCodes Diagram(s) (N)`, `Building product(s) (N)`, `Diagram`, `Primary`, image lines, `[Terms of Service](/terms)`, `[Privacy Policy](/privacy)`, the site header/nav lines at the top.
- Some long paragraphs are single source lines; some table cells appear one-per-line.
- The export is UTF-8, LF line endings, no BOM. Keep that on output.

## 3. Heading conversion (depth by R-number)

Headings have **no trailing period**.

- Section heading: `### [Section R404 Foundation and Retaining Walls](...)` → `## Section R404 Foundation and Retaining Walls`
- Subheadings derive depth from the number of R-number segments:
  - 2 segments (`R404.1`) → `###`
  - 3 segments (`R404.1.3`) → `####`
  - 4 segments (`R404.1.3.3`) → `#####`
  - 5 segments (`R404.1.3.3.6`) → `######`
- Keep the title text verbatim, minus the link. No trailing period, even if the source title looks like a sentence.

## 4. Inline text conversion

- Strip **all** `[text](url)` links, keeping the inner `text`. This applies to defined terms, cross references, table references and document references (e.g., `[California Mechanical Code]` → `California Mechanical Code`).
- Do **not** add emphasis around code-section or table references; keep them as plain text (`Section R406.2`, `Table R401.4.1(2)`).
- Preserve units and symbols verbatim:
  - SI/imperial pairs: `6 inches (152 mm)`, `1 foot (305 mm)`, `3/8-inch (9.5 mm)`, `1/1,500`, `1 square foot (0.0929 m2)`, `f'c`.
  - `m2`/`m3` appear as plain `m2`/`m3` (no superscript) — keep as-is.
  - Degree sign: `200°F (93°C)` (U+00B0).
  - Fraction formats exactly as in source: `3/8`, `1/4`, `33/8`, `1/2`.
  - Superscript footnote letters: keep **verbatim** inside table cells and table titles (e.g., `6 solidd`, `12 groutd`, `#4 at 48`, `PLAIN MASONRY FOUNDATION WALLSf`, `WHERE d ≥ 5 INCHESa, c, f`). Do not convert to markdown superscript markup.
  - `≥`/`≤` (U+2265/U+2264) render in the console as `�` under some encodings — that is a display artifact only; the file content is correct. Do not "fix" or re-encode.

## 5. Special paragraphs

- **Single exception:** `**Exception:** <text>` — bold label, colon, then the paragraph on the same line.
- **Multiple exceptions:** `**Exceptions:**` on its own line, followed by a numbered list.
- **Inline note:** `> **Note:** <text>` as a blockquote.
- **Trailing note after a section (no blockquote):** `Note: <text>` as a plain paragraph (see ch4.md `R408.8`).
- **`For SI:` lines:** keep verbatim as a plain paragraph immediately after the table or figure: `For SI: 1 inch = 25.4 mm.` Join multiple unit definitions on one line separated by commas when they belong to the same table/figure.
- **`Notes:`** on its own line, followed by a numbered list (`1.` …). Keep all note text.
- Keep California-specific content (e.g., references to the California Mechanical Code, California Building Code, California Energy Code) verbatim.

## 6. Lists

- Numbered list items start at column 0: `1. `, `2. ` …
- Nested numbered items are indented 4 spaces under the parent item (see `R408.3` item 2 sub-items).
- Bulleted sub-items under a note use 3-space dash indent (`   - ...`); this appears in `R403.1.2` Note 3 — preserve the pattern from the source.
- Preserve `Items 1–3`, `(1)`/`(2)` style enumerations as plain text inside paragraphs; do not reformat them into lists.

## 7. Tables

- Caption: `**Table R404.1.3.2(8) — MINIMUM VERTICAL REINFORCEMENT …**` (bold, `Table <ref> — <UPPERCASE TITLE>`). Keep the footnote-letter suffixes on the title (e.g., `…WALLSf`).
- Convert every data table to a pipe table:
  - Header row, then a separator row (`|---|---|`), then data rows.
  - Reconstruct multi-level headers from the one-cell-per-line source (see the 3-level examples in `R404.1.2.1(1)` and `R403.1(1)`).
  - Repeat blank group cells: when a column group header spans rows, carry the value down or repeat it as shown in the exemplars.
  - `R404.2.3` uses a two-lines-per-`Gradea`-column pattern that flattens to a 9-column pipe table — when a column header is split across two source lines, merge them into one header cell.
  - Table `R404.1.3.2(9)` was parsed programmatically: 41 rows × 16 columns of `#bar at spacing` values — confirm the exact cell count per row when a table is very wide; a mismatch means rows were dropped.
- **Every** `**Table …**` caption must be immediately followed (after blank lines) by a pipe-table header row starting with `|`. Figures (`**Figure R…**`) are captions only, followed by their `For SI:` line and `Notes:` — never a pipe table.
- Table footnotes: plain paragraph `For SI: …` then `Notes:` numbered list. Keep `R`/`NR` legend text (e.g., `R = Continuous … required.`, `NR = Continuous footings not required.`) and `DR = Design Required` in Notes verbatim.

## 8. Noise removal (must be deleted)

- `UpCodes Diagram(s) (N)` and `UpCodes Diagram (N)` lines.
- `Building product(s) (N)` lines.
- `Diagram`, `Primary`, `Category`, image/thumbnail lines, and any bare `N` line that is page chrome (not a table group-header).
- Site header/nav lines at the top of the export and the trailing `[Terms of Service]`/`[Privacy Policy]` links.
- Any dangling `<!-- CHUNK -->` / `<!-- NEXT -->` scaffolding markers (they are only used mid-conversion to stage chunks).

## 9. Procedure

1. Save the full chapter export as one UTF-8 text file (LF, no BOM).
2. Inventory headings and tables first (regex `^### \[` for headings, `\[TABLE R` or caption patterns for tables). Map line numbers so nothing is missed.
3. Convert section by section, top to bottom, applying rules 3–8.
4. Stage into a temp file (`C:\Users\kjwil\AppData\Local\Temp\opencode\`) chunk by chunk, joining chunks on a `<!-- NEXT -->` marker, then remove markers at the end.
5. Append into the target `2025_crc/chN.md` by replacing a single trailing `<!-- CHUNK -->` marker.
6. Run the verification checklist (section 10) before declaring done.

## 10. Verification checklist

Run these greps against the finished file — every one must return **zero** matches:

- `\]\(` — no leftover links
- `UpCodes`, `Diagram`, `Building product`, `^Primary`, `^Category`
- `\.jpg`, `\.png`, `\.gif`
- `CHUNK`, `NEXT`
- `^(Exception|Exceptions):` — non-bold exception labels (they must all be `**Exception:**` / `**Exceptions:**`)

Structural checks:

- `## Section R4xx` headings cover the full chapter through the last section (e.g., R401…R408).
- Every `**Table` caption line is followed (after blank lines) by a line starting with `|`.
- Headings strictly follow depth-by-R-number (rule 3); no trailing periods on headings.
- `For SI:` lines and `Notes:` lists present where the source had them.

## 11. Known pitfalls

- The raw export is large (Chapter 4 ≈ 263 KB / 9.2 K lines). Subagents have failed this conversion twice; do it carefully in chunks, verifying after each chunk.
- Do **not** reuse the overwritten original: if the raw export was overwritten during chunked editing, it is lost (git-untracked, Recycle Bin empty). Save the full export to a separate file _before_ editing the target.
- When flattening wide tables, count cells per row; a dropped group header silently shifts all data columns.
- Keep table footnote letters as plain text — converting them to `^a` markdown breaks the mapping to Notes.
- Preserve exact spacing inside SI parentheticals (`not less than 1 foot (305 mm)`) — do not normalize units or spacing.
