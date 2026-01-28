from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

def load_env_file(env_path: str | Path = ".env") -> None:
    """Carrega variáveis de um arquivo .env simples se existir."""
    path = Path(env_path)
    if not path.exists():
        return
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, _, val = stripped.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception as exc:  # noqa: BLE001
        print(f"[env] Não foi possível carregar .env: {exc}")


load_env_file()

print(os.getenv("FALKORDB_PASSWORD"))

