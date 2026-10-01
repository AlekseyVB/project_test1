# Окружения версии 2.0

Код адаптирован с **Python 3.7 на Python 3.12**. Опорная и проверенная версия Python — **3.12**; обратная совместимость с 3.7 не заявляется. Профили библиотек разделены, чтобы учебный ноутбук не требовал одновременно TensorFlow и PyTorch.

| Профиль | Уроки | Установка |
|---|---|---|
| data-analysis | Анализ заёмщиков | `requirements/data-analysis.txt` |
| pytorch | Основы, VAE, перенос стиля | `requirements/pytorch.txt` |
| tensorflow | Основы слоёв, CNN, автокодировщик, два NLP-урока | `requirements/tensorflow.txt` |

Оба deep-learning профиля используют общий `base.txt`. Версии TensorFlow, torch и torchvision закреплены совместимой парой. Остальные зависимости ограничены диапазонами; точные снимки проверочных окружений находятся в `requirements/locks/` после выполнения проверок. Снимки Windows/Linux предназначены для воспроизведения именно проверочного объединённого окружения, а не для обязательной установки всех библиотек каждому студенту.

Для точного воспроизведения проверочного объединённого окружения:

```text
# Windows, Python 3.12:
python -m pip install -r requirements/locks/windows-py312.txt
# Linux, Python 3.12; +cpu пакеты берутся из официального PyTorch индекса:
python -m pip install -r requirements/locks/linux-py312.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

## Windows PowerShell

Установите Python 3.12. В коротком пути к проекту:

```powershell
py -3.12 -m venv .venv-tf
.\.venv-tf\Scripts\python.exe -m pip install -r .\requirements\tensorflow.txt
```

Путь с большим количеством вложенных папок может вызвать ошибку установки TensorFlow: Windows ограничивает длину некоторых имён файлов. Для учебного проекта используйте короткую папку. Если проект уже в глубокой папке, отдельное окружение можно создать во временном каталоге:

```powershell
$envPath = Join-Path $env:TEMP 'ml-lab-tf'
py -3.12 -m venv $envPath
& "$envPath\Scripts\python.exe" -m pip install -r .\requirements\tensorflow.txt
```

Не требуется менять системную политику выполнения PowerShell или активировать окружение. Команды явно используют его Python.

## Linux

```bash
python3.12 -m venv .venv-tf
.venv-tf/bin/python -m pip install -r requirements/tensorflow.txt
```

Для PyTorch на Linux, если нужен только CPU, сначала установите пару из официального CPU-индекса, затем профиль:

```bash
python3.12 -m venv .venv-torch
.venv-torch/bin/python -m pip install torch==2.14.1 torchvision==0.29.1 --index-url https://download.pytorch.org/whl/cpu
.venv-torch/bin/python -m pip install -r requirements/pytorch.txt
```

Пакеты с локальным суффиксом `+cpu` удовлетворяют закреплению публичной версии без суффикса.

## VS Code и Jupyter

Установите расширения Microsoft Python и Jupyter. Откройте **корневую папку репозитория**, затем `.ipynb`. В Select Kernel выберите Python созданного окружения. Перезапускайте ядро после изменения источника данных или устройства. Выполняйте сверху вниз: скрипт автоматически находит корень и показывает графики внутри ноутбука.

Открытие через Colab возможно только с доступной копией репозитория: `ml_lab` должен быть рядом с `notebooks`. Личный Google Drive не требуется. Если нужен Colab/GPU, сначала самостоятельно скопируйте репозиторий и задайте MLLAB_ROOT; ноутбуки сами не выполняют git clone и не подключают Drive.

## Переключатели

| Переменная | По умолчанию | Значение |
|---|---|---|
| MLLAB_QUICK | 1 | Короткая проверка; 0 — исходный порядок эпох/более крупные размеры моделей. |
| MLLAB_DATA_SOURCE | demo | demo / local / builtin; поддерживаемые значения зависят от урока. |
| MLLAB_DATA_DIR | data в корне | Реальные файлы и кэш встроенных датасетов. |
| MLLAB_OUTPUT_DIR | outputs в корне | Результаты каждого урока в отдельной подпапке. |
| MLLAB_ALLOW_DOWNLOAD | 0 | Явное разрешение загрузить встроенный датасет или официальные VGG weights. |
| MLLAB_USE_GPU | 0 | Запрос GPU; для PyTorch при недоступном CUDA используется CPU. |
| MLLAB_ROOT | поиск по родителям | Корень репозитория, если блокнот открыт из другого каталога. |

Пример Windows для реального MNIST:

```powershell
$env:MLLAB_DATA_SOURCE = 'builtin'
$env:MLLAB_ALLOW_DOWNLOAD = '1'
$env:MLLAB_QUICK = '0'
```

Linux:

```bash
export MLLAB_DATA_SOURCE=builtin
export MLLAB_ALLOW_DOWNLOAD=1
export MLLAB_QUICK=0
```

Затем перезапустите ядро. Для возврата к безопасному demo сбросьте переменные или задайте `demo`, `1`, `0`, `0` соответственно для source, quick, download, use_gpu.

## GPU

CPU — переносимая базовая конфигурация. GPU требует отдельной совместимости драйвера/пакетов и не входит в CPU-проверку. Для современного TensorFlow на Windows используйте WSL2, а не старый native-Windows CUDA стек. На Linux следуйте официальным инструкциям TensorFlow. PyTorch CUDA-пару выбирайте по официальной матрице; CPU-колёса GPU не поддерживают.

- TensorFlow: https://www.tensorflow.org/install/pip
- PyTorch: https://pytorch.org/get-started/locally/
- VS Code: https://code.visualstudio.com/docs/datascience/jupyter-notebooks

## Проверки

```text
python -m unittest discover -s tests -v
python tools/run_notebooks.py --group tensorflow
python tools/run_notebooks.py --group pytorch
python tools/run_notebooks.py --group data-analysis
```

Используйте Python соответствующего окружения. `--group all` требует обеих deep-learning библиотек и предназначен для объединённого проверочного окружения. Ядра изолированы по ноутбукам, используется запускаемый интерпретатор, глобальные kernelspec не устанавливаются. Выполненные ноутбуки и JSON-отчёты сохраняются в `outputs/validation/<platform>/`.
