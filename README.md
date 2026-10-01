# Machine Learning Learning Lab — версия 2.0

Каталог учебных и исследовательских Jupyter-ноутбуков по машинному обучению,
Computer Vision, NLP и генеративным моделям. Работы сгруппированы по темам и
снабжены краткой навигацией.

**Последние изменения выполнены для использования материалов как учебных пособий
по алгоритмам анализа данных, машинного обучения и искусственного интеллекта,
с переносимым запуском в Windows и Linux.** Дата подготовки: 2026-10-01.

**Версия 2.0: код адаптирован с Python 3.7 на Python 3.12**, исправлены
учебные ошибки и обновлены API библиотек. Python 3.12 — проверенная среда запуска;
обратная совместимость с Python 3.7 не заявляется.

> Версия 2.0 — учебные материалы для Python 3.12.
> По умолчанию — короткие CPU-опыты на синтетических данных без сетевых загрузок.
> Это не промышленное решение и не подтверждение качества моделей на реальных данных.

## Четыре исправленные учебные ошибки

По пояснению автора, эти ошибки **были намеренно оставлены**, когда материалы
предоставлялись студентам, чтобы студенты находили их во время работы.

| Урок | Что исправлено в версии 2.0 |
|---|---|
| Основы PyTorch | Оптимизатор получал параметры прежней `ourNet`, хотя обучалась `ourNet2`. Теперь используется именно обучаемая сеть **(ошибка намеренно оставлялась как задание для студентов)**. |
| Классификация изображений | Задача называлась детекцией, хотя выполнялась классификация; порядок width/height при resize был перепутан. Название и форма изображений исправлены **(ошибка намеренно оставлялась как задание для студентов)**. |
| Перенос стиля | При соединении списков признаков фактически использовался только один из двух стилей. Теперь отдельно учитываются оба **(ошибка намеренно оставлялась как задание для студентов)**. |
| Классификация текстов | Порядок названий авторов не соответствовал текстам. Теперь имя, файл и метка связаны одной записью **(ошибка намеренно оставлялась как задание для студентов)**. |

Это пояснение педагогического замысла предоставлено автором; оно не выведено из истории Git.
Алгоритмы сохранены. Подробности: [CHANGELOG](docs/CHANGELOG.md).

## Каталог

### Computer Vision

| Ноутбук | Задача | Стек |
|---|---|---|
| [Классификация изображений Conv2D](notebooks/computer-vision/object-detection-conv2d.ipynb) | классификация всего изображения, не детекция; историческое имя файла сохранено | TensorFlow, Keras |
| [Neural style transfer](notebooks/computer-vision/neural-style-transfer-pytorch.ipynb) | перенос и смешивание художественных стилей | PyTorch, torchvision |

### Generative models

| Ноутбук | Задача | Стек |
|---|---|---|
| [MNIST autoencoder](notebooks/generative/autoencoder-mnist-keras.ipynb) | базовый и свёрточный автокодировщик изображений | TensorFlow, Keras |
| [FashionMNIST variational autoencoder](notebooks/generative/vae-mnist-pytorch.ipynb) | VAE и генерация изображений; сохранён FashionMNIST из исходного кода | PyTorch, torchvision |

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

1. Используйте Python 3.12 и отдельное окружение для выбранной группы.
2. Установите один профиль: `requirements/data-analysis.txt`, `tensorflow.txt` или `pytorch.txt`.
3. Откройте выбранный `.ipynb` в VS Code/Jupyter, выберите созданное ядро и выполните сверху вниз.
4. По умолчанию данные синтетические, запуск короткий и CPU-only. GPU не обязателен.
5. Для реальных данных задайте источник и каталог; загрузки разрешаются только явно.

### Windows PowerShell

Разместите проект в коротком пути: глубокие пути могут мешать установке TensorFlow.

```powershell
py -3.12 -m venv .venv-tf
.\.venv-tf\Scripts\python.exe -m pip install -r .\requirements\tensorflow.txt
.\.venv-tf\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-tf\Scripts\python.exe .\tools\run_notebooks.py --group tensorflow
```

### Linux

```bash
python3.12 -m venv .venv-tf
.venv-tf/bin/python -m pip install -r requirements/tensorflow.txt
.venv-tf/bin/python -m unittest discover -s tests -v
.venv-tf/bin/python tools/run_notebooks.py --group tensorflow
```

Для PyTorch/анализа данных используйте соответствующий профиль и группу проверки.
В VS Code требуются расширения Python и Jupyter. Активация окружения не обязательна.

Подробнее об окружениях:
[`docs/ENVIRONMENTS.md`](docs/ENVIRONMENTS.md).

Источники данных: [DATA](docs/DATA.md). Порядок обучения: [LEARNING](docs/LEARNING.md).
Фактические результаты проверок и их границы: [VALIDATION](docs/VALIDATION.md).
GitHub Actions настроен для CPU-запусков в Windows/Linux; фактический статус
удалённых проверок смотрите во вкладке Actions. GitLab содержит копию материалов;
GitHub Actions в GitLab не выполняется, отдельный GitLab CI не настроен.

## Репозитории

- Основной: [GitHub — project_test1](https://github.com/AlekseyVB/project_test1).
- Копия: [GitLab — ai_deep-learning_lessons](https://gitlab.com/personalgroupavb/ai_deep-learning_lessons).

## Ограничения

- реальные исходные наборы и обученные веса не включены;
- результаты коротких синтетических опытов не являются benchmark;
- восстановленные Windows/Linux окружения проверяются отдельно от GPU;
- полное обучение и проверка качества на реальных данных требуют отдельного запуска;
- у каталога пока нет общей лицензии.

## Исторические материалы

Исходные ноутбуки с прежними выводами сохранены в истории Git на
[коммите a842320](https://github.com/AlekseyVB/project_test1/tree/a842320f69af80a8a2aae6a867f6e0bd1e85fcab/notebooks).
Эту версию можно использовать для поиска ошибок, а версию 2.0 — для разбора исправлений.

## Автор

Алексей Бобрешов — [GitHub](https://github.com/AlekseyVB)
