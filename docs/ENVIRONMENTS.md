# Окружения для ноутбуков

## Почему нет одного requirements.txt

Каталог объединяет эксперименты на TensorFlow/Keras и PyTorch, созданные в
разное время. Один общий список зависимостей создал бы тяжёлое и потенциально
несовместимое окружение, поэтому зависимости лучше устанавливать отдельно по
тематическим группам.

## TensorFlow/Keras notebooks

К этой группе относятся:

- `object-detection-conv2d.ipynb`;
- `autoencoder-mnist-keras.ipynb`;
- `text-segmentation-keras.ipynb`;
- `text-generation-seq2seq.ipynb`;
- `keras-layer-input-output.ipynb`.

Типовой состав окружения:

```text
tensorflow
numpy
pandas
scikit-learn
matplotlib
seaborn
Pillow
```

В старых ноутбуках могут одновременно встречаться `keras` и
`tensorflow.keras`. При модернизации следует привести импорты к одному API.

## PyTorch notebooks

К этой группе относятся:

- `neural-style-transfer-pytorch.ipynb`;
- `vae-mnist-pytorch.ipynb`;
- `pytorch-starter-network.ipynb`.

Типовой состав:

```text
torch
torchvision
numpy
matplotlib
Pillow
scipy
```

Версии `torch` и `torchvision` должны выбираться совместно с учётом Python,
CUDA и используемого GPU.

## Data analysis notebook

Для `borrower-profile-analysis.ipynb` обычно нужны:

```text
numpy
pandas
scikit-learn
matplotlib
seaborn
```

## Рекомендуемый процесс модернизации

1. Создать чистое окружение для одного ноутбука.
2. Выполнить ячейки последовательно и записать реально работающие версии.
3. Заменить устаревшие API минимальными изменениями.
4. Удалить зависимость от личного Google Drive.
5. Добавить фиксированный random seed и отдельную тестовую выборку.
6. Сохранить lock-файл рядом с конкретной работой.

## Проверка внешних источников

Перед выполнением `gdown`, `git clone`, `wget`, `pip install` или загрузкой
pickle/checkpoint необходимо проверить владельца, лицензию и целостность
источника. Старые ссылки могут вести на изменившийся или недоверенный файл.
