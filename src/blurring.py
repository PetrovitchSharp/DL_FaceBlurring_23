import numpy as np
from PIL import Image, ImageDraw, ImageFilter


# https://stackoverflow.com/questions/55629643/how-to-blur-an-ellipse-with-imagedraw
def make_ellipse_mask(size, x0, y0, x1, y1, blur_radius):
    img = Image.new("L", size, color=0)
    draw = ImageDraw.Draw(img)
    draw.ellipse((x0, y0, x1, y1), fill=255)
    return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))


def blur_bbox_oval(image: Image, bbox: np.ndarray) -> Image:
    bbox = bbox.astype(int)
    overlay_image = image.filter(ImageFilter.GaussianBlur(radius=15))
    mask_image = make_ellipse_mask(
        image.size, bbox[0], bbox[1], bbox[2], bbox[3], 5
        )
    masked_image = Image.composite(overlay_image, image, mask_image)
    return masked_image
