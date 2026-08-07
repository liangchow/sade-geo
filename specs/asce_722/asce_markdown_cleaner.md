# ASCE 7-22 Markdown Cleaner — Parsing Instructions

Purpose: convert a plain-text, hard-wrapped extraction of an ASCE 7-22 chapter (e.g. `asce_722/ch20.md`) into clean, self-contained markdown suitable for consumption by agentic applications. Target norms mirror `2025_crc/crc_markdown_cleaner.md` and `2025_cbc/cbc_markdown_cleaner.md` so every code family in the corpus shares one style. This document is the canonical rule set used (and to be used) for the `asce_722/` files.

## 1. Reference files

- **Exemplar input (source format):** `asce_722/ch20.md` — Chapter 20 Site Classification Procedure for Seismic Design Purposes, plain-text extraction (139 lines). This is the shape every `asce_722/chN.md` currently has.
- **Exemplar targets (output format):** `2025_crc/ch4.md` and `2025_cbc/ch18_clean.md` — clean chapters. Match their conventions (bold `**Table …**`/`**Figure …**` captions, `**Exception:**`, pipe tables, `For SI:` lines, unwrapped paragraphs).
- **Sibling cleaners:** `2025_crc/crc_markdown_cleaner.md` and `2025_cbc/cbc_markdown_cleaner.md` — same target norms; reuse their rules where the formats overlap.

## 2. Source format characteristics (plain-text extraction)

There is **no markdown at all** in this format: no links, no `### [` headings, no pipe tables, no bold, no blockquotes. Instead:

- **Paragraphs are hard-wrapped at ~75 chars.** A logical paragraph spans many lines; the next heading, list item, `EXCEPTION` or page footer begins at the start of a wrapped line. There are essentially no blank-line separators inside the body (blank lines occur only before the numbered list at `20.2.1` and around the equation block).
- **Section headings inline at column 0:**
  - Main sections are all-caps: `20.1 SITE CLASSIFICATION`, `20.2 SITE CLASS DEFINITIONS`, `20.3 ESTIMATION OF SHEAR WAVE VELOCITY PROFILES`, `20.4 DEFINITIONS OF SITE CLASS PARAMETERS`, `20.5 CONSENSUS STANDARDS AND OTHER REFERENCED DOCUMENTS`.
  - Subsections are mixed-case with the **body paragraph glued onto the same line** after the title: `20.2.1 Site Class F Where any of the following conditions is satisfied, the site shall be classified as …` → heading is `Site Class F`, body is `Where any of the following conditions is satisfied, …`.
- **Numbered list** (the `20.2.1` Site Class F conditions, items `1.`–`4.`) starts at column 0; wrapped continuation lines are indented ~3 spaces; `EXCEPTION` sub-blocks are indented ~3 spaces.
- **`EXCEPTION:` labels** are all-caps; the body starts on the same line and continuation lines are indented.
- **Page footer chrome** appears mid-chapter: `Minimum Design Loads and Associated Criteria for Buildings and Other Structures 225` (book title + page number). Drop.
- **Equation block** (`20.4.1`): mangled OCR — the summation sign renders as `P`, the fraction is split across three indented lines, and `=1` subscripts are flattened (`Pni =1 diPni =1` / `di` / `vsi`). The equation number `(20.4-1)` sits on its own line, followed by a `where` variable list.
- **Symbols:** `̄vs` = U+0304 (combining macron) + `vs` — keep the bytes verbatim. `≥` = U+2265. `∕` = U+2215 in `ft∕s (m∕s)`. A semicolon is used as a thousands separator in `1;000 psf` — an OCR artifact of `1,000`.
- **Table 20.2-1 is referenced but its body is NOT in this extraction.** Keep `Table 20.2-1` as plain text; do not fabricate the table.

## 3. Heading conversion

- **Main sections:** `# 20.1 SITE CLASSIFICATION` → `## Section 20.1 Site Classification` (Title Case; keep acronyms/identifiers such as `Site Class` phrasing as-is).
- **Subsections:** depth by number of dotted segments (hashes = segments + 1, same progression as the CBC cleaner); no trailing period; **strip the body text glued after the title.** For ch20 the mapped titles are:

| Source line start                                                 | Heading                                                         |
| ----------------------------------------------------------------- | --------------------------------------------------------------- |
| `20.2.1 Site Class F Where any …`                                 | `#### 20.2.1 Site Class F`                                      |
| `20.2.2 Soft Clay Site Class E Where …`                           | `#### 20.2.2 Soft Clay Site Class E`                            |
| `20.2.3 Site Classes C, CD, D, DE, and E The …`                   | `#### 20.2.3 Site Classes C, CD, D, DE, and E`                  |
| `20.2.4 Site Classes B and BC (Medium Hard and Soft Rock) Site …` | `#### 20.2.4 Site Classes B and BC (Medium Hard and Soft Rock)` |
| `20.2.5 Site Class A (Hard Rock) The …`                           | `#### 20.2.5 Site Class A (Hard Rock)`                          |
| `20.4.1 vs, Average Shear Wave Velocity The …`                    | `#### 20.4.1 vs, Average Shear Wave Velocity`                   |

- **Known print titles for ch20** (fixed titles; use this list to split title from body — never guess the boundary):
  1. `20.1 Site Classification`
  2. `20.2 Site Class Definitions`
  3. `20.2.1 Site Class F`
  4. `20.2.2 Soft Clay Site Class E`
  5. `20.2.3 Site Classes C, CD, D, DE, and E`
  6. `20.2.4 Site Classes B and BC (Medium Hard and Soft Rock)`
  7. `20.2.5 Site Class A (Hard Rock)`
  8. `20.3 Estimation of Shear Wave Velocity Profiles`
  9. `20.4 Definitions of Site Class Parameters`
  10. `20.4.1 vs, Average Shear Wave Velocity`
  11. `20.5 Consensus Standards and Other Referenced Documents`

- Insert a blank line between a heading and its body paragraph (the source has none).

## 4. Paragraph reflow (line joining)

- Join wrapped lines into a single paragraph: replace each line break with a single space, stopping at the next structural element (heading, list item, `EXCEPTION`, page footer, equation block, `where`).
- **Soft hyphenation:** when a line ends in `-` and the next line starts with lowercase and the joined word is a real word, remove the hyphen and join with no space: `para-` + `meters` → `parameters`, `liquefi-` + `able` → `liquefiable`, `stan-` + `dard` → `standard`. Keep true compound hyphens that are mid-line or real words (`site-specific`, `highly organic`). Verify every joined word against the surrounding context.
- **Do not re-wrap** the output; write each paragraph as a single long line (same as the CBC/CRC exemplars).
- Separate block elements with one blank line.

## 5. Inline content / symbols

- Keep cross references as plain text: `Table 20.2-1`, `Section 20.2`, `Section 20.4`, `Section 21.1`, `Section 11.4.2`, `Chapter 23`, `Equation (20.4-1)`. Do not add emphasis or links.
- Keep `̄vs` (U+0304 + `vs`) verbatim; keep `su`, `SDS`, `SD1`, `PI`, `H`, `w` as printed.
- `≥` (U+2265) verbatim (`w ≥40%`, `PI >75` uses plain `>`).
- `∕` (U+2215) in `ft∕s (m∕s)` verbatim.
- **Fix the OCR thousands separator:** `1;000 psf` → `1,000 psf`. Scan for other `digit;digit` pairs.
- Preserve SI parentheticals exactly: `10 ft (3.1 m)`, `100 ft (30 m)`, `25 ft (7.6 m)`, `H >10 ft (H >3 m)`. Do not normalize units or spacing.

## 6. EXCEPTION blocks

- `EXCEPTION:` (all caps, may be indented) → `**Exception:**` with the body on the same line, e.g. `**Exception:** Site response analysis is not required to determine spectral accelerations for liquefiable soils. …`.
- When an exception is nested under a numbered item, indent the `**Exception:**` paragraph 4 spaces under that item (same as CBC `1803.7`/`1809.10` style).
- Reflow the wrapped exception text onto one line.

## 7. Lists

- Numbered items start at column 0: `1. ` … `4. `, each folded onto a single line.
- Continuation lines (indented ~3 spaces) fold into the item text.
- A nested `EXCEPTION` under an item stays an indented paragraph beneath that item — never renumber it as a new list item.
- Keep `(a)`/`(b)`/`(1)` style enumerations inside paragraphs inline; do not turn them into lists.

## 8. Equations and where lists

- Keep the equation block readable rather than reproducing the mangled OCR:
  - **Label:** `**(20.4-1)**` on its own line.
  - **Formula:** reconstruct the split fraction as a single line:
    `̄vs = (Σn i=1 di) / (Σn i=1 (di / vsi))`
    (source renders `Σ` as `P` and splits numerator/denominator across three indented lines: `Pni =1 diPni =1` / `di` / `vsi`; `n i=1` is the summation bounds — `n` over `i=1`).
  - **where list** after the label, one item per line:
    - `di = Thickness of any layer between 0 and 100 ft (30 m),`
    - `vsi = Shear wave velocity in ft∕s (m∕s), and`
    - `Σn i=1 di = 100 ft (30 m).` (the source glues this onto the `vsi` line as `…, andPi =1n di = 100 ft (30 m).`).
- Apply the same reconstruction to any other `where`/equation blocks in future chapters.

## 9. Noise removal (must be deleted)

- Page footers: `Minimum Design Loads and Associated Criteria for Buildings and Other Structures 225` — regex `^Minimum Design Loads and Associated Criteria for Buildings and Other Structures \d*$` (the page number varies). Also drop any other running-head lines that are just the book title.
- There are no `.jpg`/image tokens in this format and no `<!-- CHUNK -->`/`<!-- NEXT -->` scaffolding in the finished file.

## 10. Procedure

1. Copy the raw extraction to a staging file under `C:\Users\kjwil\AppData\Local\Temp\opencode\`; never edit the target until verified.
2. Inventory first: headings (`^\d{2}\.\d`), page-footer noise, the equation block, and `EXCEPTION` lines. Map line numbers so nothing is missed.
3. Convert top to bottom, sections 3–9. Verify per chunk before moving on.
4. Append into `asce_722/chN_clean.md` by replacing a single trailing `<!-- CHUNK -->` marker (same workflow as the CBC/CRC files).
5. Run the verification checklist (section 11).

## 11. Verification checklist

Zero-match greps against the finished file:

- `\]\(` — no links
- `Minimum Design Loads` — no page footers
- `Pni\b|Pi =1|P\s*i\s*=1` — no mangled summation tokens
- `\d;\d` — no semicolon thousands separators
- `\.jpg`, `\.png`, `\.gif`
- `CHUNK`, `NEXT`
- `^EXCEPTION` — all labels converted to `**Exception:**`
- `^20\.[1-5]\s` — no unconverted headings (must be `## Section 20.x` / `#### 20.x.y`)

Structural checks:

- `## Section 20.1 Site Classification` … `## Section 20.5 Consensus Standards and Other Referenced Documents` present in order.
- `#### 20.2.1` … `#### 20.4.1` subsections present, with the body split off the heading line.
- Every paragraph is a single unwrapped line.
- `**(20.4-1)**` label and the three-item `where` list present; `̄vs` kept verbatim.

## 12. Known pitfalls

- **Heading/body glued:** subsection bodies start on the same line as the title; only the fixed print titles (section 3) separate title from body — never guess.
- **Soft hyphenation:** `para-meters`, `liquefi-able`, `stan-dard` are PDF syllable splits, not real hyphens; joining them wrong corrupts words.
- **OCR summation:** `Pni =1` is `Σn i=1` and the fraction layout is lost — reconstruct `(20.4-1)` exactly as specified in section 8.
- **Page footers:** book-title + page-number lines appear mid-chapter and are easy to mistake for body text.
- **Combining macron:** `̄vs` is U+0304 followed by `vs`; some fonts/consoles display it oddly — keep the bytes.
- **Semicolon thousands separator:** `1;000 psf` → `1,000 psf`; scan the whole chapter.
- **Missing table bodies:** `Table 20.2-1` and other tables are referenced but not extracted; keep references as plain text, do not fabricate tables.
