import sys
from pathlib import Path

# Add the Worker directory to sys.path so 'src' can be imported
worker_dir = Path(__file__).parent.parent
sys.path.insert(0, str(worker_dir))
