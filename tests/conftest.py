import sys
from pathlib import Path

# Adiciona a raiz do projeto ao PYTHONPATH para permitir imports "from src..."
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
