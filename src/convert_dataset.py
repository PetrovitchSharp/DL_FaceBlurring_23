import json
from pathlib import Path
from typing import Dict

import cv2


def convert_WIDER_face_dataset_to_COCO_format(
    filename: str,
    image_path: Path
) -> Dict:
    ''' Convert WIDER Face dataset to COCO format '''
    with open(filename) as f:
        lines = f.readlines()

    categories = [{
        'id': 1,
        'name': 'face',
        'supercategory': 'face'
    }]
    images = []
    annotations = []

    image_id = 0
    anno_id = 0
    i = 0
    while i < len(lines):
        # Image info
        img_name = lines[i].strip()
        img = cv2.imread(str(image_path / img_name))
        image = {
            'id': image_id,
            'file_name': img_name,
            'height': img.shape[0],
            'width': img.shape[1]
            }
        images.append(image)
        i += 1

        # Number of faces on image
        num_anno = int(lines[i].strip())
        i += 1
        if num_anno == 0:
            i += 1
            continue

        # Annotations
        for _ in range(num_anno):
            anno = {'id': anno_id,
                    'image_id': image_id,
                    'category_id': 1,
                    'iscrowd': 0}

            bbox = [int(el) for el in lines[i].strip().split()][:4]
            area = bbox[2] * bbox[3]
            anno['area'] = area
            anno['bbox'] = bbox
            annotations.append(anno)
            anno_id += 1
            i += 1
        image_id += 1
    return {
        'images': images,
        'annotations': annotations,
        'categories': categories
    }


def main():
    train_wider_face = 'data/wider_face_split/wider_face_train_bbx_gt.txt'
    image_path = Path('data/WIDER_train/images')

    coco_annotations = convert_WIDER_face_dataset_to_COCO_format(
        train_wider_face, image_path)

    print('Converting train dataset...')
    with open('data/wider_face_train.json', 'w') as f:
        json.dump(coco_annotations, f)

    print('Converting val dataset...')
    val_wider_face = 'data/wider_face_split/wider_face_val_bbx_gt.txt'
    image_path = Path('data/WIDER_val/images')

    coco_annotations = convert_WIDER_face_dataset_to_COCO_format(
        val_wider_face, image_path)

    with open('data/wider_face_val.json', 'w') as f:
        json.dump(coco_annotations, f)


if __name__ == '__main__':
    main()
