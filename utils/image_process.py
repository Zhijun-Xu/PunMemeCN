# -*- coding:utf-8 -*-
import os
import random
from PIL import Image
from copy import deepcopy
from matplotlib import pyplot as plt
from .json_process import save_json_file


def resize_image(image, square:bool=True, size:int=224):
    """
    Resize image to a given size^2 \n
    If square is true, the image will first be filled into a square shape.
    """
    image = deepcopy(image)
    if square is True:
        width, height = image.size
        _size = max(width, height)
        new_image = Image.new("RGB", (_size, _size), (255, 255, 255))
        new_image.paste(image, box=((_size - width)//2, (_size - height)//2))  # upper left corner
        image = new_image
    image = image.resize((size, size), Image.LANCZOS)
    return image


def random_4panels(img_folder:str, save_path:str, random_seed:int=2024, total_nums:int=100):
    """
    Randomly select four images from the dataset to create a four-panel image, \n
     and document the random focused panel and focused object. \n
    0: Top left, 1: Top right, 2: Bottom left, 3: Bottom right
    """
    imgs = os.listdir(img_folder)
    random.seed(random_seed)
    record = dict()
    record['img_folder'] = img_folder
    record['instances'] = dict()
    # Randomly obtain 4 panels image
    for i in range(total_nums):
        temp_imgs = deepcopy(imgs)
        random.shuffle(temp_imgs)
        _4panels = temp_imgs[0:4]
        # Focused panel, we care about what's in the panel.
        focused_panel = random.randint(0,len(_4panels)-1)
        # Focused object, we care where the object is
        focused_object = random.randint(0,len(_4panels)-1)
        # Record
        instance_key = f'{i+1:0{len(str(total_nums))+1}d}'
        record['instances'][instance_key] = \
            {'4panels':_4panels, 'focused_panel':focused_panel, 'focused_object':focused_object}
    # Save
    save_json_file(record, save_path)


def get_4panel_image(img_folder:str, _4panels:list, size:int=448, margin:int=4, show:bool=False):
    """
    Generate a 4-panel image based on the order in the '_4panels' list. \n
    [image_0, image_1, image_2, image_3]  \n
    0: Top left, 1: Top right, 2: Bottom left, 3: Bottom right
    """
    assert len(_4panels) == 4
    sub_images = []
    sub_size = (size - 4*margin) // 2
    for img in _4panels:
        sub_image = Image.open(os.path.join(img_folder, img))
        sub_image = resize_image(image=sub_image, size=sub_size)
        sub_images.append(sub_image)
    panels_image = Image.new("RGB", (size, size), (255, 255, 255))
    # Top Left
    image_top_left = sub_images[0]
    anchor_x = margin
    anchor_y = margin
    panels_image.paste(image_top_left, box=(anchor_x, anchor_y))
    # Top Right
    image_top_right = sub_images[1]
    anchor_x = size - margin -sub_size
    anchor_y = margin
    panels_image.paste(image_top_right, box=(anchor_x, anchor_y))
    # Bottom Left
    image_bottom_left = sub_images[2]
    anchor_x = margin
    anchor_y = size - margin -sub_size
    panels_image.paste(image_bottom_left, box=(anchor_x, anchor_y))
    # Bottom Right
    image_bottom_right = sub_images[3]
    anchor_x = size - margin -sub_size
    anchor_y = size - margin -sub_size
    panels_image.paste(image_bottom_right, box=(anchor_x, anchor_y))

    if show is True:
        plt.figure(); plt.imshow(panels_image); plt.show()
    return panels_image


def get_4image_list(img_folder:str, _4panels:list, size:int=224, show:bool=False):
    """
    Generate a list containing 4 images based on the order in the '_4panels' list. \n
    [image_0, image_1, image_2, image_3]
    """
    assert len(_4panels) == 4
    images = []
    for img in _4panels:
        sub_image = Image.open(os.path.join(img_folder, img))
        sub_image = resize_image(image=sub_image, size=size)
        images.append(sub_image)
    if show is True:
        for image in images:
            plt.figure(); plt.imshow(image); plt.show()
    return images

