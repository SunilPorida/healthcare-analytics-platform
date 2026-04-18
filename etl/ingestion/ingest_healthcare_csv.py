"""
Ingest healthcare CSV datasets from a local folder that simulates an S3 raw bucket.

``data/raw`` acts as the simulated S3 prefix (no network calls). Cleaned tables are
written to ``data/processed``.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

# Simulated S3 raw bucket → local directory (repository root relative)
REPO_ROOT = Path(__file__).resolve().parents[2]
SIMULATED_S3_RAW_PREFIX = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

DEFAULT_HEALTHCARE_CSV = "healthcare_dataset.csv"

LOGGER = logging.getLogger(__name__)


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _ensure_processed_dir() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    LOGGER.debug("Processed output directory ready: %s", PROCESSED_DIR)


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Lightweight cleaning suitable for a raw→processed landing step."""
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    out = out.dropna(how="all")
    return out


def _resolve_csv_paths(raw_dir: Path, explicit_file: str | None) -> list[Path]:
    if explicit_file:
        candidate = Path(explicit_file)
        path = candidate if candidate.is_absolute() else raw_dir / candidate
        if not path.exists():
            LOGGER.warning(
                "Expected CSV not found (simulated S3 key missing): %s",
                path,
            )
            return []
        if not path.is_file():
            LOGGER.warning("Path is not a file, skipping: %s", path)
            return []
        return [path]

    if not raw_dir.exists():
        LOGGER.warning(
            "Simulated S3 raw prefix does not exist; create it or add data: %s",
            raw_dir,
        )
        return []

    paths = sorted(raw_dir.glob("*.csv"))
    if not paths:
        LOGGER.warning("No CSV files under simulated S3 raw prefix: %s", raw_dir)
        return []

    LOGGER.info("Discovered %d CSV file(s) under %s", len(paths), raw_dir)
    return paths


def ingest_csv(path: Path) -> Path | None:
    """Load one CSV, clean, and write to processed. Returns output path or None on failure."""
    LOGGER.info("Starting ingestion: %s", path)
    try:
        df = pd.read_csv(path, low_memory=False)
    except FileNotFoundError:
        LOGGER.error("File disappeared during read: %s", path)
        return None
    except pd.errors.EmptyDataError:
        LOGGER.warning("Empty CSV (no rows): %s", path)
        return None
    except Exception:
        LOGGER.exception("Failed to read CSV: %s", path)
        return None

    LOGGER.info("Loaded rows=%d, columns=%d", len(df), len(df.columns))
    cleaned = _clean_dataframe(df)
    LOGGER.info("After cleaning: rows=%d, columns=%d", len(cleaned), len(cleaned.columns))

    out_name = f"{path.stem}_cleaned.csv"
    out_path = PROCESSED_DIR / out_name
    try:
        cleaned.to_csv(out_path, index=False)
    except Exception:
        LOGGER.exception("Failed to write processed CSV: %s", out_path)
        return None

    LOGGER.info("Wrote processed dataset: %s", out_path)
    return out_path


def run(
    *,
    raw_dir: Path = SIMULATED_S3_RAW_PREFIX,
    input_name: str | None = None,
    discover_all: bool = False,
) -> list[Path]:
    """
    Run ingestion. If ``input_name`` is set, only that file under ``raw_dir`` is used.
    If ``discover_all`` is True, all ``*.csv`` in ``raw_dir`` are ingested.
    Otherwise defaults to ``healthcare_dataset.csv`` if present; if missing, falls back
    to all CSVs in the folder (still graceful if none).
    """
    LOGGER.info(
        "Using simulated S3 raw prefix (local): %s",
        raw_dir.resolve(),
    )
    _ensure_processed_dir()

    if discover_all:
        paths = _resolve_csv_paths(raw_dir, explicit_file=None)
    elif input_name:
        paths = _resolve_csv_paths(raw_dir, explicit_file=input_name)
    else:
        default_path = raw_dir / DEFAULT_HEALTHCARE_CSV
        if default_path.exists():
            paths = [default_path]
            LOGGER.info("Using default healthcare dataset: %s", default_path.name)
        else:
            LOGGER.warning(
                "Default healthcare CSV not found: %s — attempting all CSVs in raw folder",
                default_path,
            )
            paths = _resolve_csv_paths(raw_dir, explicit_file=None)

    outputs: list[Path] = []
    for p in paths:
        out = ingest_csv(p)
        if out is not None:
            outputs.append(out)

    if not paths:
        LOGGER.info("Ingestion finished: no input files to process.")
    elif not outputs:
        LOGGER.info("Ingestion finished: no outputs written (all reads failed or empty).")
    else:
        LOGGER.info("Ingestion finished: %d file(s) written.", len(outputs))

    return outputs


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest healthcare CSVs from data/raw (simulated S3) into data/processed.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=SIMULATED_S3_RAW_PREFIX,
        help="Local folder simulating the S3 raw bucket/prefix (default: repo data/raw).",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help=f"CSV filename under raw dir (default: try {DEFAULT_HEALTHCARE_CSV} then all *.csv).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="discover_all",
        help="Ingest every *.csv in the raw folder.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Debug logging.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    _configure_logging(args.verbose)

    run(
        raw_dir=args.raw_dir,
        input_name=args.input,
        discover_all=args.discover_all,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
