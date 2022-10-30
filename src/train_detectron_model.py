import argparse
import os

# import some common detectron2 utilities
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.data.datasets import register_coco_instances
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator
from detectron2.utils.logger import setup_logger


setup_logger()


def build_evaluator(cfg, dataset_name, output_folder=None):
    """
    Create COCO Evaluator
    """
    if output_folder is None:
        output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
    evaluator_type = MetadataCatalog.get(dataset_name).evaluator_type
    if evaluator_type in ["coco", "coco_panoptic_seg"]:
        return COCOEvaluator(dataset_name, output_dir=output_folder)


class Trainer(DefaultTrainer):
    """
    We use the "DefaultTrainer" which contains pre-defined default logic for
    standard training workflow. They may not work for you, especially if you
    are working on a new research project. In that case you can write your
    own training loop. You can use "tools/plain_train_net.py" as an example.
    """

    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        return build_evaluator(cfg, dataset_name, output_folder)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--cfg',
        type=str,
        help='path to config file',
        default='configs/faster_rcnn_R_50_FPN.yaml')
    args = parser.parse_args()
    register_coco_instances(
        "wider_face_train", {},
        "data/wider_face_train.json",
        "data/WIDER_train/images")
    register_coco_instances(
        "wider_face_val", {},
        "data/wider_face_val.json",
        "data/WIDER_val/images")

    cfg = get_cfg()
    cfg.merge_from_file(args.cfg)

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = Trainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()


if __name__ == "__main__":
    main()
