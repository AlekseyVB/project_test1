"""Portable paths, explicit data sources and reproducible teaching fixtures.

Demo fixtures are synthetic and must not be reported as real-world benchmarks.
No helper downloads data or executes shell commands.
"""
from dataclasses import dataclass
import json
import os
from pathlib import Path
import random

import numpy as np
from PIL import Image


def find_root(start=None):
    start = Path(start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / 'ml_lab' / 'runtime.py').is_file() and (candidate / 'notebooks').is_dir():
            return candidate
    raise FileNotFoundError('Откройте папку project_test1 или задайте MLLAB_ROOT.')


def env_bool(name, default=False):
    raw = os.environ.get(name)
    if raw is None:
        return default
    if raw.lower() not in {'1', '0', 'true', 'false', 'yes', 'no'}:
        raise ValueError(f'{name}: используйте 1/0 или true/false')
    return raw.lower() in {'1', 'true', 'yes'}


@dataclass(frozen=True)
class Settings:
    root: Path
    data: Path
    output: Path
    quick: bool
    source: str
    allow_download: bool
    use_gpu: bool
    seed: int = 42


def settings(name):
    root = find_root(os.environ.get('MLLAB_ROOT'))
    source = os.environ.get('MLLAB_DATA_SOURCE', 'demo')
    if source not in {'demo', 'local', 'builtin'}:
        raise ValueError('MLLAB_DATA_SOURCE: demo, local или builtin')
    output = Path(os.environ.get('MLLAB_OUTPUT_DIR', str(root / 'outputs'))).expanduser().resolve() / name
    output.mkdir(parents=True, exist_ok=True)
    cfg = Settings(root, Path(os.environ.get('MLLAB_DATA_DIR', str(root / 'data'))).expanduser().resolve(),
                   output, env_bool('MLLAB_QUICK', True), source,
                   env_bool('MLLAB_ALLOW_DOWNLOAD'), env_bool('MLLAB_USE_GPU'))
    random.seed(cfg.seed)
    np.random.seed(cfg.seed)
    # Notebook plots should be visible in VS Code/Jupyter, including validation outputs.
    try:
        from IPython import get_ipython
        shell = get_ipython()
        if getattr(shell, 'kernel', None) is not None:
            shell.run_line_magic('matplotlib', 'inline')
    except ImportError:
        pass
    print(f'Версия 20 | source={cfg.source} | quick={cfg.quick} | GPU requested={cfg.use_gpu}')
    if source == 'demo':
        print('Синтетические учебные данные: результаты не являются оценкой качества на реальном датасете.')
    return cfg


def tensorflow_setup(cfg):
    os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
    os.environ.setdefault('KERAS_HOME', str(cfg.root / '.cache' / 'keras'))
    if not cfg.use_gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    import tensorflow as tf
    tf.keras.utils.set_random_seed(cfg.seed)
    tf.config.threading.set_inter_op_parallelism_threads(2)
    tf.config.threading.set_intra_op_parallelism_threads(2)
    print('TensorFlow', tf.__version__, '| devices:', tf.config.list_physical_devices())
    return tf


def torch_setup(cfg):
    os.environ.setdefault('TORCH_HOME', str(cfg.root / '.cache' / 'torch'))
    import torch
    torch.manual_seed(cfg.seed)
    torch.set_num_threads(2)
    device = torch.device('cuda' if cfg.use_gpu and torch.cuda.is_available() else 'cpu')
    if device.type == 'cuda':
        torch.cuda.manual_seed_all(cfg.seed)
    print('PyTorch', torch.__version__, '| device:', device)
    return torch, device


def resize_gray(path, height=32, width=64):
    with Image.open(path) as image:
        array = np.asarray(image.convert('L').resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    return array[..., None] / 255.0


def demo_images(count=160, height=32, width=64, classes=2, seed=42):
    rng = np.random.default_rng(seed)
    labels = np.arange(count) % classes
    images = rng.uniform(0, 0.12, (count, height, width, 1)).astype('float32')
    for i, label in enumerate(labels):
        column = 2 + int(label) * max(1, (width - 8) // classes)
        images[i, 3:height-3, column:column+4, 0] = 0.9
    return images, labels


def author_windows(tokens, length, step):
    if length < 1 or step < 1:
        raise ValueError('length и step должны быть положительными')
    return [tokens[i:i+length] for i in range(0, len(tokens)-length+1, step)]


def document_split(labels, seed=42):
    """Split each author's independent documents before making text windows."""
    rng = np.random.default_rng(seed)
    groups = [[], [], []]
    labels = np.asarray(labels)
    for label in np.unique(labels):
        indices = rng.permutation(np.flatnonzero(labels == label))
        if len(indices) < 3:
            raise ValueError('Для каждого класса нужны минимум три независимых документа')
        train_count = min(len(indices)-2, max(1, int(len(indices)*.6)))
        val_count = min(len(indices)-train_count-1, max(1, int(len(indices)*.2)))
        for group, values in zip(groups, [indices[:train_count], indices[train_count:train_count+val_count], indices[train_count+val_count:]]):
            group.extend(values.tolist())
    return tuple(np.array(group, dtype=int) for group in groups)


def load_mnist(cfg, tf):
    cache = cfg.data / 'mnist.npz'
    if not cache.is_file():
        if not cfg.allow_download:
            raise FileNotFoundError('Поместите mnist.npz в MLLAB_DATA_DIR или явно разрешите MLLAB_ALLOW_DOWNLOAD=1.')
        # Official Keras MNIST source and SHA-256, verified in Keras 3.15.1.
        tf.keras.utils.get_file(fname='mnist.npz',
            origin='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
            file_hash='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1',
            hash_algorithm='sha256', cache_dir=str(cfg.data), cache_subdir='')
    with np.load(cache, allow_pickle=False) as data:
        return data['x_train'], data['x_test']


def author_documents(cfg):
    """Records and label order come from one manifest, not two parallel lists."""
    if cfg.source == 'demo':
        names = [f'Демо-класс {i}' for i in range(6)]
        words = ['лес река сосна', 'город улица дом', 'звезда космос планета',
                 'кофе чашка стол', 'море корабль ветер', 'книга слово письмо']
        records = [(f'{words[label]} текст номер {i} ' * 20, label)
                   for label in range(6) for i in range(12)]
        return names, records
    if cfg.source != 'local':
        raise ValueError('Для текстов используйте demo или local')
    manifest = cfg.data / 'authors.json'
    mapping = json.loads(manifest.read_text(encoding='utf-8'))
    if not isinstance(mapping, dict) or len(mapping) < 2:
        raise ValueError('authors.json должен содержать минимум два автора')
    names = list(mapping)
    records = []
    seen = set()
    for label, name in enumerate(names):
        paths = mapping[name]
        if not isinstance(paths, list) or len(paths) < 3:
            raise ValueError(f'{name}: нужны минимум три отдельных документа')
        for path in paths:
            resolved = (cfg.data / path).resolve()
            if not resolved.is_relative_to(cfg.data):
                raise ValueError('Путь документа должен оставаться внутри MLLAB_DATA_DIR')
            if resolved in seen:
                raise ValueError('Один документ не должен принадлежать нескольким записям manifest')
            seen.add(resolved)
            text = resolved.read_text(encoding='utf-8').strip()
            if not text:
                raise ValueError(f'Пустой текст: {resolved.name}')
            records.append((text, label))
    return names, records
