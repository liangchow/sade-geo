# CBC Markdown Cleaner — Parsing Instructions

Purpose: convert a block-format text extraction of a 2025 California Building Code (CBC) chapter into clean, self-contained markdown suitable for consumption by agentic applications. The target conventions mirror `2025_crc/crc_markdown_cleaner.md` and the exemplar `2025_crc/ch4.md`, so both California code families produce one consistent corpus style.

This document is the canonical rule set used (and to be used) for the `2025_cbc/` files. **Do not apply the CRC cleaner verbatim to CBC files** — see section 14 for the format differences.

## 1. Reference files

- **Exemplar input (source format):** `2025_cbc/ch18.md` — Chapter 18 Soils and Foundations, block-format extraction (2,052 lines). This is the shape every `2025_cbc/chN.md` currently has.
- **Exemplar target (output format):** `2025_crc/ch4.md` — clean Chapter 4 (R401–R408). Match its conventions exactly.
- **Sibling cleaner:** `2025_crc/crc_markdown_cleaner.md` — same target norms; reuse its rules where the two input formats overlap (sections 5, 7, 8, 13 of that doc).

## 2. Source format characteristics (CBC block extraction)

Unlike the CRC UpCodes export, the CBC extraction contains **no markdown links** (`](`)`, no `### [` headings, no pipe tables, and no UpCodes noise lines**. It is plain text with:

- Header chrome lines at the very top: a zero-width space (U+200B), `Search 2025 California Building Code …`, a breadcrumb line, `CHAPTER 18 SOILS AND FOUNDATIONS`.
- Matrix adoption table as a columnar, space-aligned grid; continuation rows are prefixed with `> ` blockquotes.
- Section divisions as all-caps lines: `SECTION 1801—GENERAL` (em-dash U+2014; the section title can wrap to the following all-caps line, e.g. `SECTION 1806—PRESUMPTIVE LOAD-BEARING` / `VALUES OF SOILS`).
- Numbered section headings as plain lines with a trailing period: `1801.1 Scope.`, `1803.1.1.1 Preliminary soil report.` — the body paragraph begins on the next line (no blank line).
- Agency adoption tags as `[...]` plain text: `[OSHPD 1R, 2 & 5]`, `[HCD 1]`, `[HCD 1/AC]`, `[DSA SS]`, `[SFM 1]`, `[OSHPD 2]`. They appear at paragraph start, inline, as standalone lines, and inside table rows. Keep them verbatim.
- Table captions as all-caps lines with lettered footnote suffixes: `TABLE 1807.1.6.2—CONCRETE FOUNDATION WALLSb, c`.
- Tables as **columnar blocks**: wrapped all-caps header lines, then data rows with space-separated cells (no `|`), e.g. `5 4 PC PC PC PC PC PC PC PC PC`. `For SI:` appears as the last line of the block.
- Lettered table footnotes as separate paragraphs: `a.For design lateral soil loads, see Section 1610.` (letter directly attached, no space).
- Figure captions: `FIGURE 1808.7.1—FOUNDATION CLEARANCES FROM SLOPES` followed by an image line `FIGURE 1808.7.1.jpg` (drop the `.jpg` line).
- Equation images: lines like `Eq0087.jpgEquation 18-2` (image token glued to a label). The math is not recoverable.
- Numbered list items are glued: `1.Text` (no space after the period) in the majority of cases, `1. Text` in a few.
- Cross references are plain text: `Section 1803.5.10`, `Table 1808.8.1`, `Figure 1808.7.1`, `Chapter 19`, `Section 1613`.
- File is UTF-8, LF line endings, no BOM. Keep that on output.

## 3. Front matter conversion

1. **Drop header chrome:** the zero-width-space line, `Search 2025 …`, breadcrumb line, and the first `CHAPTER 18 SOILS AND FOUNDATIONS` duplicate. Keep the second, real title block.
2. **Chapter H1:** `CHAPTER 18` / `SOILS AND FOUNDATIONS` → `# Chapter 18 — Soils and Foundations` (em-dash, title case; mirrors CRC `# Chapter 4 — Foundations`).
3. **Matrix adoption table:** convert the columnar grids into pipe tables, mirroring CRC `ch4.md` lines 7–28:
   - `## Matrix Adoption Table` heading, then the nonregulatory note paragraph.
   - Table 1 — adopting-agency grid: `| Adopting agency | BSC | BSC-CG | SFM | … |` with a single data row of adopted-value codes. Drop the `> ` blockquote prefixes on continuation rows.
   - Table 2 — adoption actions: `| Adoption action | | |` with `X` marks.
   - Table 3 — adopted sections: `| Chapter / Section | Adopted |` with one row per section (e.g. `| 1808.8.1 | X |`).
   - Keep the `†` symbol note (`> The state agency does not adopt sections identified with the following symbol: †`).
4. **State Fire Marshal preamble:** keep as a plain paragraph (`The Office of the State Fire Marshal’s adoption …`).
5. **About / user notes:** `About this chapter:` → `## About this chapter` + paragraph. `User notes:` → `## User notes` + following paragraphs. `ICC code development note:` → plain paragraph starting `ICC code development note:`.

## 4. Section heading conversion

- **SECTION divisions:** `SECTION 1801—GENERAL` → `## Section 1801 General`.
  - Join a wrapped title first: `SECTION 1806—PRESUMPTIVE LOAD-BEARING` + `VALUES OF SOILS` → `## Section 1806 Presumptive Load-Bearing Values of Soils`.
  - Convert the ALL-CAPS title to Title Case, preserving all-caps acronyms and identifiers (VSC, CLSM, OSHPD, CPT/SPT, f′c, A–F). Example: `GEOTECHNICAL INVESTIGATIONS` → `Geotechnical Investigations`.
  - A division may carry a trailing agency tag: `SECTION 1811—PRESTRESSED ROCK AND SOIL FOUNDATION ANCHORS [OSHPD 1R, 2 & 5]` → `## Section 1811 Prestressed Rock and Soil Foundation Anchors [OSHPD 1R, 2 & 5]` (keep the tag verbatim).
- **Numbered headings:** depth by number of segments after the 4-digit section number, no trailing period:
  - `1801.1 Scope.` (2 segments) → `### 1801.1 Scope`
  - `1803.1.1 Preliminary soil report.` (3 segments) → `#### 1803.1.1 Preliminary Soil Report`
  - `1803.1.1.1 Preliminary soil report.` (4 segments) → `##### 1803.1.1.1 Preliminary Soil Report`
  - (5 segments would be `######`; none occur in ch18 but use the same progression.)
  - Keep the title verbatim except: strip the trailing period, and remove the `>` blockquote prefixes if present.
  - Insert a blank line between the heading and its body paragraph (the source has none).
- **Detection guard:** a numbered heading always starts with a 4-digit section number followed by a dot and digits (`^\d{4}\.`). Table data rows start with a single number (`1. Crystalline …`) or bare values (`5 4 PC …`) and only occur inside a TABLE block — never treat those as headings.

## 5. Inline content

- Keep all cross references as plain text: `Section 1803.5.10`, `Table 1808.8.1`, `Figure 1808.7.1`, `Chapter 19`, `Section 1613`. Do not add emphasis or links.
- Keep agency tags verbatim, in place: `[OSHPD 1R, 2 & 5] Not permitted by OSHPD. …`; inline `…the soil shall be made under the responsible charge of a California registered geotechnical engineer. [OSHPD 1R, 2 & 5] …`; standalone `[OSHPD 2] – For applications listed in Section 1.10.2.`.
- Preserve symbols and identifiers exactly as printed: `f ′c`, `f′m`, `tf′m`, `fy`, `f′c`, `1/2-inch (12.7 mm)`, `11/2 inches` (sic), `3/8 inch`, `200°F (93°C)` (U+00B0), `m2`/`m3` plain, `1/1,500`, `33.3-percent slope`.
- Curly apostrophes (U+2019) are used (`building official’s`) — keep them; do not "fix" to straight quotes.
- Some source characters display as `�?`/`�` in a console but are valid UTF-8 (e.g. `10'` is the digits `10` + U+2019; em-dash is U+2014). Do not re-encode; the file content is correct.

## 6. Special paragraphs

- **Single exception:** `Exception: …` → `**Exception:** …` (bold label, colon, same-line text).
- **Multiple exceptions:** `Exceptions:` on its own line, then a numbered list (`1. …`). Preserve nested sub-paragraphs under an item verbatim (see ch18.md `1803.7` item 2).
- **`For SI:` lines:** keep as a plain paragraph immediately after the table/figure block; join multiple unit definitions on one line with commas (`For SI: 1 inch = 25.4 mm, 1 foot = 304.8 mm, 1 pound per square foot per foot = 0.157 kPa/m.`).
- **Table footnotes:** lettered paragraphs `a.`, `b.`, … — keep the letter scheme verbatim (the superscripts in the caption and cells map to these letters). Normalize the spacing to `a. ` (letter, period, space). They stay as plain paragraphs, **not** a `Notes:` numbered list, because the letter→cell mapping would break.
- **`Notes:`/`Note:` blocks in body text:** keep verbatim; numbered sub-items follow the list rules in section 7.

## 7. Lists

- Normalize every numbered item from the glued form to `1. `: `1.Text` → `1. Text`, `9.The depth of soil compaction elements …` → `9. The depth of soil compaction elements …`.
- Items are separate paragraphs in the source (blank-line separated in many places); collapse to a single tight list with one blank line before the list and one after.
- Nested items are indented 4 spaces under the parent item.
- Do not convert `(a)`, `(1)`, `a.`, `b.` enumerations inside a paragraph into lists — keep them inline.

## 8. Tables (columnar block → pipe table)

- Caption: `**Table 1807.1.6.2 — CONCRETE FOUNDATION WALLSb, c**` (bold, `Table <ref> — <UPPERCASE TITLE>`, em-dash with spaces, footnote letters kept on the title).
- Reconstruct the header stack from the wrapped all-caps header lines. Rules of thumb:
  - A group header spans the following sub-column lines (e.g. `MINIMUM VERTICAL REINFORCEMENT-BAR SIZE AND SPACING (inches)` spans `Design lateral soil loada (psf per foot of depth)` which spans `30d 45d 60`, each of which spans the `Minimum wall thickness (inches)` line `7.5 9.5 11.5`).
  - Join wrapped header words into one cell (`MAXIMUM` + `WALL` + `HEIGHT` + `(feet)` → `Maximum wall height (feet)`); normalize to title case while keeping symbols and footnote letters.
  - When a sub-column line lists bare values (`30d 45d 60`, `7.5 9.5 11.5`), emit one header cell per value (with its footnote letter).
- Data rows: split on runs of whitespace. When a row line repeats the leading key (e.g. `5 4 PC …` then next line `5 PC …`), the second line omits the repeated group key — repeat it down / carry it (same as the CRC one-cell-per-line rule). ch18 examples: `Table 1807.1.6.2` repeats the wall-height column; `Table 1806.2` carries the numbered row prefix.
- **Two-column tables with multi-line rows** (e.g. `Table 1808.8.1`, minimum compressive strength): a single logical row spans several lines — the item text (possibly with a bracketed agency tag and a sub-letter like `2a.`/`2b.`) and the value at the end (`2,500 psi`). Merge the item text into one cell and the trailing value into the second column.
- Cell tokens like `PC`, `9d`, `10 (solidc)`, `Note d`, `—` must be preserved verbatim (footnote letters are part of the token).
- The `For SI:` line ends the block. Lettered footnotes follow it.
- **Every** `**Table …**` caption must be immediately followed (after blank lines) by a pipe-table header row starting with `|`.

## 9. Figures and equations

- `**Figure 1808.7.1 — FOUNDATION CLEARANCES FROM SLOPES**` for the caption (em-dash with spaces), followed by its `For SI:` line. Drop the adjacent `FIGURE 1808.7.1.jpg` image line.
- Equation image lines (`Eq0087.jpgEquation 18-2`, `Eq0100.jpgEquation 18-4`, `For SI: Eq0107.jpg`): drop the image token; retain the label as plain text (`Equation 18-2`). The math itself is not recoverable — do not invent it.

## 10. Noise removal (must be deleted)

- The zero-width-space line (U+200B) and all search/nav/breadcrumb lines at the top.
- `.jpg` image references (figure and equation image tokens).
- Any leading `> ` blockquote markers when the row is actually table content (keep the `†` note blockquote).
- Duplicate `CHAPTER N` title lines from the header chrome.
- Dangling conversion scaffolding (`<!-- CHUNK -->`, `<!-- NEXT -->`) if present mid-conversion.

## 11. Procedure

1. Copy the block extraction to a staging file under `C:\Users\kjwil\AppData\Local\Temp\opencode\`; never edit the target until verified.
2. Inventory with greps first (so nothing is missed): `^SECTION `, `^\d{4}\.` headings, `^TABLE `, `^FIGURE `, `\.jpg`, `^Exception`, `^1\.`/`^1\.\s` list items.
3. Convert top to bottom, sections 3–10. Verify per chunk before moving on.
4. Append into `2025_cbc/chN.md` by replacing a single trailing `<!-- CHUNK -->` marker (as the CRC file did).
5. Run the verification checklist (section 12).

## 12. Verification checklist

Zero-match greps against the finished file:

- `\.jpg`, `\.png`, `\.gif`
- `\]\(` (no links introduced)
- `^FIGURE ` (all figures now `**Figure …**` captions)
- `^SECTION ` (all converted to `## Section …`)
- `^1[78]\d\d\.\w` — glued numbered headings without a following space or markdown prefix
- `^1[0-9]\.\w` — glued list items without a space
- `^(Exception|Exceptions):` — non-bold exception labels (must all be `**Exception:**`/`**Exceptions:**`)
- `CHUNK`, `NEXT`, `Search 2025`

Structural checks:

- `# Chapter 18 — …` H1 present; `## About this chapter`, `## Matrix Adoption Table`, `## User notes` present as appropriate.
- All `## Section 18xx` divisions in order, 1801…1813, each with correct Title Case.
- Every `**Table` and `**Figure` caption is followed (after blank lines) by a `|` pipe table (tables) or its `For SI:` line (figures).
- Every agency tag `[… ]` still present where the source had it.
- Lettered table footnotes still map to the caption/cell letters.

## 13. Known pitfalls

- **Wrong cleaner:** the CRC cleaner finds nothing in this format (0 links, 0 `### [` headings, 0 pipes) and misses everything this format needs. Always use this document for `2025_cbc/` files.
- **Section-title wraps:** `SECTION 1806—PRESUMPTIVE LOAD-BEARING` / `VALUES OF SOILS` — always check the next line for a wrapped all-caps continuation before converting.
- **Headings vs table rows:** `^\d{4}\.` vs `1. Crystalline …` — only 4-digit-prefixed lines are headings; table rows live inside TABLE blocks.
- **Glued list items** (`1.Text`) are easy to miss; normalize them all or the list breaks.
- **Multi-line table rows** (1808.8.1 style) silently lose the value column if merged incorrectly — verify column parity after conversion.
- **Console misread:** em-dash (U+2014), curly apostrophe (U+2019), and prime (`′`) render as `�`/`-`/`?` in some consoles. The file bytes are correct; do not "fix" them.
- **Sub-letter rows** `2a.`/`2b.` in tables keep their letters — they are not separate top-level items.
- Preserve exact SI parentheticals (`not less than 1 foot (305 mm)`); do not normalize spacing or units.
