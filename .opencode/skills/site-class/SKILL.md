---
name: site-class
description: Determine the ASCE 7-22 site class (A, B, BC, C, CD, D, DE, E, F) from the Vs30 value in input/results.md. Use when the user asks about "site class", "Vs30", "ASCE 7-22", "soil class", or references input/results.md or Table 20.2-1.
---

# ASCE 7-22 Site Class Determination

Follow the authoritative workflow in `specs/asce_722/site_class_from_results.md`. This skill summarizes the steps for quick reference.

## Procedure

1. **Locate Vs30** in `input/results.md`. Find the line matching:
   ```
   - **Vs30 (Shear-wave velocity)**: `<number>` (meters/second)
   ```
   Extract the numeric value as `vs30_m_s`.

2. **Convert m/s to ft/s** using the exact multiplier:
   ```
   vs30_ft_s = vs30_m_s * 3.28084
   ```

3. **Look up Table 20.2-1** in `specs/asce_722/ch20.md` (Section 20.2, lines 43-55):

   | Site Class | vs (ft/s) |
   |------------|-----------|
   | A | > 5,000 |
   | B | > 3,000 to 5,000 |
   | BC | > 2,100 to 3,000 |
   | C | > 1,450 to 2,100 |
   | CD | > 1,000 to 1,450 |
   | D | > 700 to 1,000 |
   | DE | > 500 to 700 |
   | E | <= 500 |
   | F | Section 20.2.1 criteria |

   Boundary rule: `500` ft/s is E (E is `<= 500`); `700` ft/s is D (D is `> 700 to 1,000`).

4. **Report** the Site Class with: raw Vs30 (m/s), conversion (`* 3.28084`), converted value (ft/s), the matched table row, and file references to `input/results.md` and Table 20.2-1 in `specs/asce_722/ch20.md`.

## Scope

Use the Vs30-based lookup as the default. Do NOT apply the qualitative overrides from Sections 20.2.1 (Site Class F) or 20.2.2 (Site Class E) unless the user explicitly asks, even if `input/results.md` shows `Liq: True`. If asked to consider liquefaction, note the F-criteria conflict per Section 20.2.1 and the fundamental-period exception.

## Example

`Vs30 = 225.6 m/s` -> `225.6 * 3.28084 = 740.16 ft/s` -> matches `> 700 to 1,000` -> **Site Class D**.
