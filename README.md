# DL_FaceBlurring_23
Бот для замыливания лиц на фотографии


# Задача детекции лиц

### <p>Мы использовали модели из пакета [Detectron2](https://huggingface.co/datasets/wider_face/tree/main) и дообучали их на датасете [Wider Face](https://huggingface.co/datasets/wider_face/tree/main).</p><br>

<p> Мы выбрали Detectron2 для этого проекта, так как это популярная библиотека, разработанная компанией facebook, и в ней доступно множество моделей, из которых можно выбрать наиболее подходящую в зависимости от того, что будет необходимо оптимизировать в проекте - качество или скорость.<p>

## Результаты экспериментов с 3 моделями:

В качестве метрик качества детекции были выбраны метрики AP (Average precision):

1. AP - Average precision
2. AP50 - Average precision при IoU > 0.5
3. AP75 - Average precision при IoU > 0.75
4. APs - Average precision на малых по площади объектах
5. APm - Average precision на средних по площади объектах 
6. APl - Average precision на больших по площади объектах

Было произведено сравнение моделей [Faster RCNN R 50 FPN, Faster RCNN R 101 FPN](https://paperswithcode.com/lib/detectron2/faster-r-cnn) и [Retina Net R 101 FPN](https://paperswithcode.com/model/retinanet?variant=retinanet-r101-3x) при различных значениях learning rate


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

<p>Чуть лучшее качество имеет модель faster_rcnn_R_101_FPN с lr = 0.002, поэтому далее будем использовать именно ее.</p><br>

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

Предобученную модель вы можете скачать с [гугл диска](https://drive.google.com/file/d/1GoRCh9oiy3fLYwvrkR-glF0XCiRYxlJ0/view?usp=share_link). Для её использования вам необходимо прописать в конфиг бота путь к распакованной модели

# Запуск примера инференса
Для запуска инференса на CPU необходимо в файле configs/faster_rcnn_R_101_FPN.yaml заменить DEVICE с cuda на cpu

1. Запуск инференса для примера из example/example.jpg. Результат будет сохранен в файл example/blurred_example.jpg

        python src/sample_inference.py

# Скорость инференса на RTX 3090

| Model |   sec / image   |
| --- | --- |
| faster_rcnn_R_50_FPN | 0.027309 |
| faster_rcnn_R_101_FPN | 0.035943  |
| retinanet_R_101_FPN | 0.035934 |

Один GPU может в секунду обработать около 28 изображений в секунду. Можно обучить более легкую модель, если будет необходимо масштабировать решение.

# Запуск бота 

Для запуска бота необходимо добавить в settings.ini все необходимые пути и токен для бота. Затем необходимо запустить скрипт src/bot_main.py

Пример работы бота:

![Before start](https://sun9-east.userapi.com/sun9-35/s/v1/ig2/MX0acB_ZrZFP5H6DEPdi31iQRo6yUOFP6DIVzXp1b2RtuoqZyedQXkQg-pBE9pd-LshTFbcIHSLSbSsszF_M7sXA.jpg?size=720x1600&quality=95&type=album)

![Start](https://sun9-east.userapi.com/sun9-26/s/v1/ig2/4cnaa0hup0N2dSbeeeHhqSXelZq6RCNyT6A6vhVB-_9rlbRJfaXn2QtOyk1cG4CxnCkpNplnO8SHNfFBjKEaymLZ.jpg?size=720x1600&quality=95&type=album)

![RickRolled](https://sun9-east.userapi.com/sun9-32/s/v1/ig2/joYqKt07cZqVRvNdtSBEnIewFGU-tDW7sSc-eqNNGp0X3qOhSARFDyW3XLlHfs7rrgHtdcuC3VCyVgrzHCjJXfiB.jpg?size=720x1600&quality=95&type=album)

# Требуемое оборудование

Для развертывания бота необходим хостинг с видеокартой, поддерживающей технологию CUDA. В случае отсуствия поддержки этой технологии быстродействие бота не гарантируется