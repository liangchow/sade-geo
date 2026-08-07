# Instructions: Determine ASCE 7-22 Site Class from input/results.md

## Purpose

Use this workflow when asked to determine an ASCE 7-22 site class. It tells the assistant how to:

1. read `Vs30` from `input/results.md` in meters per second (m/s),
2. convert `Vs30` from m/s to ft/s by multiplying by `3.28084`,
3. look up the converted value in **Table 20.2-1** from `specs/asce_722/ch20.md`, and
4. report the Site Class and the reasoning clearly.

## Source Files

- Input data: [input/results.md](https://github.com/liangchow/sade-geo/input/results.md)
- Reference chapter + Table 20.2-1: [specs/asce_722/ch20.md](https://github.com/liangchow/sade-geo/specs/asce_722/ch20.md)

## Step-by-Step Procedure

### 1. Locate Vs30 in results.md

Open `input/results.md` and find the line that reports Vs30.

Expected pattern:

```text
- **Vs30 (Shear-wave velocity):** `<number>` (meters/second)
```

Extract the numeric value. Call it `vs30_m_s`.

### 2. Convert Vs30 from m/s to ft/s

Convert `vs30_m_s` to feet per second using:

```text
vs30_ft_s = vs30_m_s * 3.28084
```

Use the exact multiplier `3.28084` (do not approximate).

Report:
- raw Vs30 in m/s from source,
- converted Vs30 in ft/s,
- the conversion used (`* 3.28084`).

### 3. Resolve Site Class using Table 20.2-1

Refer to Table 20.2-1 in `specs/asce_722/ch20.md`. The velocity thresholds (in ft/s) are:

| Site Class | ̄vs (ft/s) |
|------------|----------------------------|
| A | > 5,000 |
| B | > 3,000 to 5,000 |
| BC | > 2,100 to 3,000 |
| C | > 1,450 to 2,100 |
| CD | > 1,000 to 1,450 |
| D | > 700 to 1,000 |
| DE | > 500 to 700 |
| E | ≤ 500 |
| F | Section 20.2.1 criteria |

Rules to apply:
- Use the upper and lower bounds exactly as written, including strict vs non-strict inequality at E.
- If the value lands exactly on a boundary, pick the class that the rule satisfies. For example, exactly 500 ft/s is **E**, because E is `≤ 500`. Exactly 700 ft/s is **D**, because D is `> 700 to 1,000` and DE is `> 500 to 700`.
- Use this Vs30-based lookup to determine the default site class from the table. Do not override with other classes (F, E, etc.) unless the user explicitly asks to apply the additional qualitative criteria from Sections 20.2.1 or 20.2.2.

### 4. Produce a structured answer

Every response should include:

1. **Vs30 from results.md** (value and unit)
2. **Conversion** (m/s → ft/s with `* 3.28084`)
3. **Converted Vs30** (value in ft/s)
4. **Table 20.2-1 lookup** (which row matches)
5. **Determined Site Class** (single letter/letter pair)
6. **Citation references** to:
   - [input/results.md](https://github.com/liangchow/sade-geo/input/results.md)
   - Table 20.2-1 in [specs/asce_722/ch20.md](https://github.com/liangchow/sade-geo/specs/asce_722/ch20.md#L43-L55)

## Example Prompt Template

Use the following instruction when asking the assistant to perform this workflow:

> Determine the ASCE 7-22 Site Class using instructions in specs/asce_722/site_class_from_results.md. Read Vs30 from input/results.md in m/s, convert to ft/s by multiplying by 3.28084, then look up Table 20.2-1 in specs/asce_722/ch20.md and report the site class with full calculations and file references.

## Example Calculation (for verification only)

If `input/results.md` contains:

```text
- **Vs30 (Shear-wave velocity):** `225.6` (meters/second)
```

then:

```text
vs30_m_s = 225.6
vs30_ft_s = 225.6 * 3.28084 = 740.16 ft/s
```

and lookup against Table 20.2-1 gives **Site Class D** because `740.16 > 700 to 1,000`.

## Acceptance Criteria

A correct response must:
- cite the Vs30 number directly from [input/results.md](https://github.com/liangchow/sade-geo/input/results.md),
- convert to ft/s using multiplication by `3.28084`,
- match the converted value to the correct row in Table 20.2-1 from [ch20.md](https://github.com/liangchow/sade-geo/specs/asce_722/ch20.md#L43-L55), and
- output a single Site Class label (A, B, BC, C, CD, D, DE, E, or F/Vs30-exception path if requested).
