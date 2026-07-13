# Machine Learning Learning Lab

Каталог учебных и исследовательских Jupyter-ноутбуков по машинному обучению,
Computer Vision, NLP и генеративным моделям. Работы сгруппированы по темам и
снабжены краткой навигацией.

> Статус: архив учебных экспериментов. Ноутбуки отражают этапы обучения и
> рассчитаны преимущественно на Google Colab; некоторые зависимости и внешние
> датасеты требуют обновления.

## Каталог

### Computer Vision

| Ноутбук | Задача | Стек |
|---|---|---|
| [Object detection with Conv2D](notebooks/computer-vision/object-detection-conv2d.ipynb) | классификация/детекция объектов свёрточной сетью | TensorFlow, Keras |
| [Neural style transfer](notebooks/computer-vision/neural-style-transfer-pytorch.ipynb) | перенос и смешивание художественных стилей | PyTorch, torchvision |

### Generative models

| Ноутбук | Задача | Стек |
|---|---|---|
| [MNIST autoencoder](notebooks/generative/autoencoder-mnist-keras.ipynb) | базовый и свёрточный автокодировщик изображений | TensorFlow, Keras |
| [MNIST variational autoencoder](notebooks/generative/vae-mnist-pytorch.ipynb) | вариационный автокодировщик и генерация цифр | PyTorch, torchvision |

### Natural Language Processing

| Ноутбук | Задача | Стек |
|---|---|---|
| [Text segmentation](notebooks/nlp/text-segmentation-keras.ipynb) | классификация текстов по авторам | Keras, embeddings |
| [Text generation](notebooks/nlp/text-generation-seq2seq.ipynb) | генерация ответов encoder-decoder моделью | Keras, LSTM |

### Data Analysis

| Ноутбук | Задача | Стек |
|---|---|---|
| [Borrower profile analysis](notebooks/data-analysis/borrower-profile-analysis.ipynb) | поиск характеристик заёмщика и сравнение моделей | Pandas, scikit-learn |

### Framework fundamentals

| Ноутбук | Задача | Стек |
|---|---|---|
| [Keras layers: input and output](notebooks/fundamentals/keras-layer-input-output.ipynb) | примеры Dense, Conv, pooling, embeddings и LSTM | TensorFlow, Keras |
| [PyTorch starter network](notebooks/fundamentals/pytorch-starter-network.ipynb) | базовая нейросеть и цикл обучения | PyTorch |

## Как пользоваться каталогом

1. Откройте выбранный `.ipynb` непосредственно на GitHub или в Google Colab.
2. Прочитайте первые Markdown-ячейки и проверьте пути к данным.
3. Создайте отдельное окружение под конкретный ноутбук.
4. Устанавливайте зависимости только после проверки старых версий и внешних
   ссылок.
5. Не выполняйте весь ноутбук автоматически, если он скачивает данные или код
   из внешних источников.

Подробнее об окружениях:
[`docs/ENVIRONMENTS.md`](docs/ENVIRONMENTS.md).

## Ограничения

- исходные наборы данных и обученные веса включены не для всех работ;
- часть путей привязана к Google Drive автора;
- версии Python и библиотек исходных запусков не зафиксированы;
- сохранённые метрики относятся к учебным экспериментам и не являются
  сопоставимым benchmark;
- некоторые API TensorFlow, Keras, PyTorch и torchvision могли измениться;
- у каталога пока нет общей лицензии.

## Возможное развитие

- выбрать 3–4 наиболее показательных ноутбука и сделать их воспроизводимыми;
- удалить секреты, личные пути и недоступные ссылки;
- добавить небольшие открытые датасеты или инструкции их получения;
- сохранить проверенные lock-файлы окружений по темам;
- экспортировать основные выводы, графики и метрики в README каждой работы;
- добавить автоматическую проверку структуры notebook JSON.

## Автор

Алексей Бобрешов — [GitHub](https://github.com/AlekseyVB)
