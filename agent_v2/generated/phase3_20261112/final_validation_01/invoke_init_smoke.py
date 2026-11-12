"""Only relocate evidence for the unchanged synthetic/test-only Init smoke."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from agent_v2.tests import real_smoke

real_smoke.GENERATED = Path(__file__).resolve().parent / 'init_runs'
raise SystemExit(real_smoke.main())
