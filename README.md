# DL_FaceBlurring_23
Бот для замыливания лиц на фотографии


# Задача детекции лиц

### <p>Мы использовали модели из пакета [Detectron2](https://huggingface.co/datasets/wider_face/tree/main) и дообучали их на датасете [Wider Face](https://huggingface.co/datasets/wider_face/tree/main).</p><br>

<p> Мы выбрали Detectron2 для этого проекта, так как это популярная библиотека, разработанная компанией facebook, и в ней доступно множество моделей, из которых можно выбрать наиболее подходящую в зависимости от того, что будет необходимо оптимизировать в проекте - качество или скорость.<p>

## Результаты экспериментов с 3 моделями:


| Model | LR |   AP   |  AP50  |  AP75  |  APs   |  APm   |  APl   |
| --- | --- | --- | --- | --- | --- | --- | --- |
| faster_rcnn_R_50_FPN | 0.001 | 25.836 | 46.442 | 26.422 | 14.243 | 51.954 | 64.173 |
| faster_rcnn_R_50_FPN | 0.002 | 29.808 | 56.563 | 28.486 | 18.259 | 55.719 | 65.323 |
| faster_rcnn_R_50_FPN | 0.004 | 27.222 | 49.653 | 27.524 | 15.839 | 53.570 | 64.207 |
| faster_rcnn_R_101_FPN | 0.001 | 26.319 | 47.563 | 26.600 | 14.617 | 52.709 | 65.282 |
| faster_rcnn_R_101_FPN | 0.002 | 30.116 | 56.954 | 28.821 | 18.188 | 56.415 | 66.945 |
| faster_rcnn_R_101_FPN | 0.004 | 28.259 | 50.657 | 28.645 | 16.616 | 54.755 | 65.891 |
| retinanet_R_101_FPN | 0.001 | 19.309 | 28.661 | 23.416 | 5.967 | 51.358 | 64.885 |
| retinanet_R_101_FPN | 0.002 | 30.106 | 54.910 | 30.166 | 16.891 | 59.845 | 69.292 |
| retinanet_R_101_FPN | 0.004 | 20.012 | 29.655 | 24.456 | 6.317 | 52.953 | 65.990 |

<p>Чуть лучшее качество имеет модель faster_rcnn_R_101_FPN, поэтому далее будем использовать именно ее.</p><br>

# Установка зависимостей

1. git clone git clone git@github.com:PetrovitchSharp/DL_FaceBlurring_23.git
1. git submodule init
1. git submodule update
1. python -m venv env
1. source env/bin/activate
1. pip install -r requirements.txt
1. python -m pip install -e detectron2

# Запуск обучения модели

1. Скачайте датасет [Wider Face](https://huggingface.co/datasets/wider_face/tree/main). Разархивируйте файлы **WIDER_train.zip**, **WIDER_val.zip** и **wider_face_split.zip** в папку **data**.
1. Запустите скрипт src/convert_dataset.py для конвертации датасета в формат COCO (сохранение json файла) (его запуск занимает до 2 минут на Ryzen 5900x):

        python src/convert_dataset.py
1. Запустите скрипт для обучения модели (конфиги лежат в папке configs), можно указать конкретный config через параметр **--config**. По-умолчанию используется модель **faster_rcnn_R_101_FPN**:

        python src/train_detection_model.py

Обучение модели занимает около 45 минут на GPU RTX3090.

# Запуск примера инференса
1. Запуск инференса для примера из example/example.jpg. Результат будет сохранен в файл example/blurred_example.jpg

        python src/sample_inference.py

# Скорость инференса на RTX 3090

| Model |   sec / image   |
| --- | --- |
| faster_rcnn_R_50_FPN | 0.027309 |
| faster_rcnn_R_101_FPN | 0.035943  |
| retinanet_R_101_FPN | 0.035934 |

Один GPU может в секунду обработать около 28 изображений в секунду. Можно обучить более легкую модель, если будет необходимо масштабировать решение.
