"""Run notebooks in isolated kernels with explicit demo/CPU settings.

Uses the interpreter running this tool; never installs global kernel specs.
No network/data/model download is permitted in the default validation mode.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager


ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'tensorflow': ['keras-layer-input-output', 'object-detection-conv2d',
                   'autoencoder-mnist-keras', 'text-segmentation-keras', 'text-generation-seq2seq'],
    'pytorch': ['pytorch-starter-network', 'neural-style-transfer-pytorch', 'vae-mnist-pytorch'],
    'data-analysis': ['borrower-profile-analysis'],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', choices=['all', *GROUPS], default='all')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    output = ROOT / 'outputs' / 'validation' / platform.system().lower()
    output.mkdir(parents=True, exist_ok=True)
    for folder in ['ipython', 'jupyter', 'keras', 'torch', 'matplotlib']:
        (ROOT / '.cache' / folder).mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, MLLAB_ROOT=str(ROOT), MLLAB_DATA_SOURCE='demo',
               MLLAB_QUICK='1', MLLAB_ALLOW_DOWNLOAD='0', MLLAB_USE_GPU='0',
               MPLBACKEND='Agg', PYTHONIOENCODING='utf-8',
               KERAS_HOME=str(ROOT / '.cache' / 'keras'),
               IPYTHONDIR=str(ROOT / '.cache' / 'ipython'),
               JUPYTER_RUNTIME_DIR=str(ROOT / '.cache' / 'jupyter'),
               TORCH_HOME=str(ROOT / '.cache' / 'torch'))
    env['MPLCONFIGDIR'] = str(ROOT / '.cache' / 'matplotlib')
    chosen = set(GROUPS[args.group]) if args.group != 'all' else None
    results = []
    for path in sorted((ROOT / 'notebooks').rglob('*.ipynb')):
        if chosen is not None and path.stem not in chosen:
            continue
        started = time.monotonic()
        entry = {'notebook': path.relative_to(ROOT).as_posix()}
        notebook = nbformat.read(path, as_version=4)
        # Avoid accidentally using an unrelated globally registered Python kernel.
        manager = KernelManager(kernel_name='python3', ip='127.0.0.1')
        manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
        client = NotebookClient(notebook, km=manager, timeout=args.timeout,
                                resources={'metadata': {'path': str(ROOT)}})
        try:
            client.execute(env=env)
            nbformat.write(notebook, output / path.name)
            entry['status'] = 'passed'
        except Exception as exc:
            entry['status'] = 'failed'
            entry['error'] = str(exc)
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
            entry['seconds'] = round(time.monotonic() - started, 2)
            results.append(entry)
            print(json.dumps(entry, ensure_ascii=False), flush=True)
    report = {'version': '2.0', 'platform': platform.platform(), 'python': sys.version,
              'mode': 'synthetic demo / quick / CPU / no downloads',
              'group': args.group, 'results': results}
    destination = args.report or output / f'{args.group}-report.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if not results or any(r['status'] != 'passed' for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
