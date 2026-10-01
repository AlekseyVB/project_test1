import ast
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import nbformat
import numpy as np
from PIL import Image
from ml_lab.runtime import Settings, author_documents, author_windows, demo_images, document_split, env_bool, find_root, load_mnist, resize_gray

ROOT = Path(__file__).resolve().parents[1]


class RuntimeTests(unittest.TestCase):
    def test_root_from_nested_notebook(self):
        self.assertEqual(find_root(ROOT / 'notebooks' / 'nlp'), ROOT)

    def test_width_height_regression(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'non-square.png'
            a = np.zeros((10, 30), dtype='uint8'); a[:, 15:] = 255
            Image.fromarray(a).save(path)
            resized = resize_gray(path, height=10, width=30)
            self.assertEqual(resized.shape, (10, 30, 1))
            self.assertEqual(float(resized[2, 20, 0]), 1.)
            self.assertEqual(float(resized[2, 5, 0]), 0.)

    def test_demo_reproducibility(self):
        a, labels_a = demo_images(seed=17); b, labels_b = demo_images(seed=17)
        np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(labels_a, labels_b)

    def test_window_boundaries(self):
        self.assertEqual(author_windows(list(range(7)), 3, 2), [[0, 1, 2], [2, 3, 4], [4, 5, 6]])
        with self.assertRaises(ValueError): author_windows([1, 2], 0, 1)

    def test_class_manifest_alignment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            mapping = {'Автор Б': ['b1.txt', 'b2.txt', 'b3.txt'], 'Автор А': ['a1.txt', 'a2.txt', 'a3.txt']}
            for name, paths in mapping.items():
                for path in paths: (root / path).write_text(name, encoding='utf-8')
            (root / 'authors.json').write_text(json.dumps(mapping, ensure_ascii=False), encoding='utf-8')
            cfg = Settings(ROOT, root, root, True, 'local', False, False)
            names, records = author_documents(cfg)
            for text, label in records: self.assertEqual(text, names[label])

    def test_invalid_bool(self):
        with patch.dict(os.environ, {'MLLAB_QUICK': 'maybe'}):
            with self.assertRaises(ValueError): env_bool('MLLAB_QUICK')

    def test_document_split_no_leakage(self):
        labels = np.repeat(np.arange(6), 3)
        train, val, test = document_split(labels)
        self.assertFalse(set(train) & set(val) or set(train) & set(test) or set(val) & set(test))
        self.assertEqual(set(train) | set(val) | set(test), set(range(18)))
        for split in (train, val, test): self.assertEqual(set(labels[split]), set(range(6)))

    def test_local_mnist_without_download(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            np.savez(path / 'mnist.npz', x_train=np.zeros((3, 28, 28), dtype='uint8'), x_test=np.zeros((2, 28, 28), dtype='uint8'))
            cfg = Settings(ROOT, path, path, True, 'builtin', False, False)
            train, test = load_mnist(cfg, None)
            self.assertEqual(train.shape, (3, 28, 28)); self.assertEqual(test.shape, (2, 28, 28))

    def test_download_requires_permission(self):
        with tempfile.TemporaryDirectory() as folder:
            cfg = Settings(ROOT, Path(folder), Path(folder), True, 'builtin', False, False)
            with self.assertRaises(FileNotFoundError): load_mnist(cfg, None)

    def test_notebook_schema_and_syntax(self):
        notebooks = list((ROOT / 'notebooks').rglob('*.ipynb'))
        self.assertEqual(len(notebooks), 9)
        for path in notebooks:
            nb = nbformat.read(path, as_version=4); nbformat.validate(nb)
            self.assertEqual(nb.metadata.ml_lab.version, '2.0')
            self.assertEqual(nb.cells[0].cell_type, 'markdown')
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    ast.parse(cell.source)
                    self.assertNotIn('drive.mount', cell.source)
                    self.assertNotIn('/content/', cell.source)
                    self.assertFalse(cell.outputs)


if __name__ == '__main__':
    unittest.main()
