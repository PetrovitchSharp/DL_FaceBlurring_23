from models import DetectronBlurringModel


def main():
    model = DetectronBlurringModel.load_model(
        'configs/faster_rcnn_R_101_FPN.yaml',
        'detectron2_output/faster_rcnn_R_101_FPN/model_final.pth')

    img_path = 'example/example.jpg'

    blurred_path = model.blur_image(str(img_path))
    print(f'Check result at {blurred_path}')


if __name__ == '__main__':
    main()
