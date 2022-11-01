from pathlib import Path
from typing import Any

import cv2
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from PIL import Image

from blurring import blur_bbox_oval


class BlurringModel:
    '''Basic class for models'''
    def __init__(self, model: Any) -> None:
        '''
        Blurring model initialization

        Args:
            model: Blurring model
        '''
        pass

    def blur_image(self, path_to_image: str) -> str:
        '''
        Blur input photo

        Args:
            path_to_image: Path to saved photo

        Returns:
            Path to blurred photo
        '''
        pass


class DetectronBlurringModel(BlurringModel):
    @classmethod
    def load_model(cls,
                   config_path: Path = 'configs/faster_rcnn_R_101_FPN.yaml',
                   model_path: Path = None):
        ''' 
        Load Detectron2 model

        Args:
            config_path: Path to model's config
            model_path:  Path to model's weights

        Returns:
            Loaded Detectron model
        '''
        cfg = get_cfg()
        cfg.merge_from_file(config_path)

        if model_path is not None:
            cfg.MODEL.WEIGHTS = str(model_path)

        predictor = DefaultPredictor(cfg)
        print(predictor)

        return cls(predictor)

    def __init__(self, model: Any) -> None:
        super().__init__(model)
        self.predictor = model

    def blur_image(self, path_to_image: str) -> str:
        '''
        Blur input photo

        Args:
            path_to_image: Path to saved photo

        Returns:
            Path to blurred photo
        '''
        img_path = Path(path_to_image)
        im = cv2.imread(path_to_image)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        # Getting predicted bounding boxes
        # with faces inside them
        outputs = self.predictor(im)
        bboxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()

        image = Image.fromarray(im)

        # Adding blurred ellipses on image
        for bbox in bboxes:
            image = blur_bbox_oval(image, bbox)

        # Saving blurred image
        blurred_path = img_path.parent / f'blurred_{img_path.name}'
        image.save(blurred_path)

        return str(blurred_path)
