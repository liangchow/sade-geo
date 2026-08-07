import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

_VS30_PATTERN = re.compile(
    r"Vs30"
    r"[^:=]*"
    r"[:=]"
    r"\s*"
    r"`?"
    r"(?P<value>[0-9]+(?:\.[0-9]+)?)"
    r"`?"
    r"(?:"
    r"\s*\("
    r"(?P<unit>[^)]*)"
    r"\)"
    r")?"
)


@dataclass(frozen=True)
class Vs30Reading:
    value: float
    unit: str | None
    value_ft_s: float


def _normalize_unit(raw_unit: str | None) -> str | None:
    if raw_unit is None:
        return None
    unit = raw_unit.strip().lower()
    if unit in {"meters/second", "m/s", "meters per second", "ms^-1", "m s^-1"}:
        return "m/s"
    if unit in {"ft/s", "feet/second", "feet per second", "fps", "ft s^-1", "ft s^-1"}:
        return "ft/s"
    return unit


def _convert_to_ft_s(value: float, unit: str | None) -> float:
    normalized_unit = _normalize_unit(unit)
    if normalized_unit == "m/s":
        return value * 3.28084
    if normalized_unit == "ft/s":
        return value
    if normalized_unit is None:
        raise ValueError(
            f"Vs30 unit missing; cannot normalize to ft/s safely. "
            f"Raw value={value!r}."
        )
    raise ValueError(
        f"Unsupported Vs30 unit: {unit!r} (normalized={normalized_unit!r}). "
        f"Expected 'meters/second' or 'ft/s'."
    )


def extract_vs30(text: str) -> Vs30Reading:
    match = _VS30_PATTERN.search(text)
    if not match:
        snippet = text.strip().replace("\n", " ")
        if len(snippet) > 400:
            snippet = snippet[:200] + " ... " + snippet[-200:]
        raise ValueError(
            "Vs30 not found in provided markdown. "
            "Check that the label format still matches 'Vs30 ... : <number> ...', "
            "that no unexpected characters wrap the number, and that the unit "
            f"parentheses are present if required. Tail: {snippet!r}"
        )

    value = float(match.group("value"))
    raw_unit = match.group("unit")
    value_ft_s = _convert_to_ft_s(value, raw_unit)

    return Vs30Reading(
        value=value,
        unit=raw_unit.strip() if raw_unit else None,
        value_ft_s=value_ft_s,
    )


def extract_vs30_from_file(path: Union[str, Path]) -> Vs30Reading:
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Failed to read Vs30 source file {file_path}: {exc}") from exc

    try:
        return extract_vs30(text)
    except ValueError as exc:
        raise ValueError(f"Failed to parse Vs30 from {file_path}: {exc}") from exc