"""Put the upstream FASTENER clone on sys.path.

FASTENER uses flat top-level imports (``import random_utils``,
``from item import Item``), so its directory has to be importable directly
rather than as a package. Import this module before importing FASTENER::

    import _bootstrap  # noqa: F401
    from fastener import EvaluatorFactory
    from item import Item
"""
import sys
from pathlib import Path

FASTENER_DIR = Path(__file__).resolve().parent.parent / "fastener"

if not FASTENER_DIR.is_dir():
    raise RuntimeError(
        f"FASTENER clone not found at {FASTENER_DIR}. "
        "Clone it with: git clone https://github.com/klemenkenda/FASTENER fastener"
    )

if str(FASTENER_DIR) not in sys.path:
    sys.path.insert(0, str(FASTENER_DIR))
