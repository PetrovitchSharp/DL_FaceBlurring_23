import numpy as np
from PIL import Image, ImageDraw, ImageFilter


# https://stackoverflow.com/questions/55629643/how-to-blur-an-ellipse-with-imagedraw
def make_ellipse_mask(
        size: tuple[int, int],
        x0: float, y0: float,
        x1: float, y1: float,
        blur_radius: float) -> Image:
    '''
    Make ellipse mask

    Args:
        size:           Size of image
        x0, x1, y0, y1: Coordinates of points, definign bounding box
        blur_radius:    Radius of blurring

    Returns:
        Blurring mask
    '''
    img = Image.new("L", size, color=0)
    draw = ImageDraw.Draw(img)
    draw.ellipse((x0, y0, x1, y1), fill=255)
    return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))


def blur_bbox_oval(image: Image, bbox: np.ndarray) -> Image:
    '''
    Blur face inside bounding box

    Args:
        image:  Image with faces to be blurred
        bbox:   Coordinates of bounding box

    Returns:
        Image with blurred face
    '''
    bbox = bbox.astype(int)
    overlay_image = image.filter(ImageFilter.GaussianBlur(radius=15))
    mask_image = make_ellipse_mask(
        image.size, bbox[0], bbox[1], bbox[2], bbox[3], 5
    )
    masked_image = Image.composite(overlay_image, image, mask_image)
    return masked_image
