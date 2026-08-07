from pathlib import Path

from modules.parser import extract_vs30_from_file
from modules.site_classifier import classify


def main() -> None:
    reading = extract_vs30_from_file(Path("input/results.md"))
    site = classify(reading.value_ft_s)

    print(f"Vs30 (raw) = {reading.value} {reading.unit}")
    print(f"Vs30 (ft/s) = {reading.value_ft_s:.6f}")
    print(f"Site Class = {site}")


if __name__ == "__main__":
    main()