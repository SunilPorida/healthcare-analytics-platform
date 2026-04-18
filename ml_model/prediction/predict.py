"""
Scoring entrypoint. Load trained artifacts and write predictions to
warehouse tables or `data/processed` depending on latency requirements.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit("Implement scoring: load model, transform inputs, persist outputs.")


if __name__ == "__main__":
    main()
