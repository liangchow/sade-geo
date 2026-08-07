SITE_CLASS_INTERVALS = [
    ("A", 5000.0, float("inf")),
    ("B", 3000.0, 5000.0),
    ("BC", 2100.0, 3000.0),
    ("C", 1450.0, 2100.0),
    ("CD", 1000.0, 1450.0),
    ("D", 700.0, 1000.0),
    ("DE", 500.0, 700.0),
]

SITE_CLASS_E_MAX = 500.0


def classify(vs30):
    try:
        vs30_value = float(vs30)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid vs30 value for classification: {vs30!r}") from exc

    if vs30_value <= SITE_CLASS_E_MAX:
        return "E"

    for site, lower, upper in SITE_CLASS_INTERVALS:
        if lower < vs30_value <= upper:
            return site

    raise ValueError(
        f"Vs30 value {vs30_value} does not map to a known site class. "
        f"Expected values in ft/s aligned with Table 20.2-1."
    )
