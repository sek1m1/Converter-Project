# jpg_conv.py
from Folder_image.image_utils import convert_image

def convert_i_jpg(input_path, output_format="png", output_folder="outputs"):
    return convert_image(input_path, output_format, output_folder)
