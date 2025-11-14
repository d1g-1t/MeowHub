from pathlib import Path
import sys

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_BACKEND_PATH = str(_BACKEND_ROOT)
if _BACKEND_PATH not in sys.path:
	sys.path.insert(0, _BACKEND_PATH)
