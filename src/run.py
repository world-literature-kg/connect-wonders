import subprocess
import sys
from pathlib import Path
import pysparql_anything as sa

BASE = Path(__file__).parent.parent.resolve()
SCRIPT_DIR = BASE / 'src'
QUERY_DIR = BASE / 'queries'
OUTPUT_DIR = BASE / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

VENV_PYTHON = Path(sys.executable)

normalization_scripts = [
    'normalizeAuthor.py',
    'normalizeBook.py',
    'normalizeTopic.py'
]

for script in normalization_scripts:
    subprocess.run([str(VENV_PYTHON), str(SCRIPT_DIR / script)], check=True)

engine = sa.SparqlAnything()

sparql_jobs = [
    ("author.sparql", "author.ttl"),
    ("book.sparql", "book.ttl"),
    ("topic.sparql", "topic.ttl"),
]

for query_file_name, output_file_name in sparql_jobs:
    query_path = (QUERY_DIR / query_file_name).as_uri()
    output_path = str(OUTPUT_DIR / output_file_name)

    engine.run(
        query=query_path,
        output=output_path,
        format='ttl'
    )
