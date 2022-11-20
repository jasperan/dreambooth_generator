import shutil
from PIL import Image
import os

IMAGES_FOLDER_OPTIONAL="/home/ubuntu/dreambooth_nacho"


Crop_images= True
Crop_size = "512"
Crop_size=int(Crop_size)


while IMAGES_FOLDER_OPTIONAL !="" and not os.path.exists(str(IMAGES_FOLDER_OPTIONAL)):
  print('The image folder specified does not exist, use the colab file explorer to copy the path :')
  IMAGES_FOLDER_OPTIONAL=input('')

if IMAGES_FOLDER_OPTIONAL!="":
      for filename in os.listdir(IMAGES_FOLDER_OPTIONAL):
        print('Scaling down {}...'.format(filename))
        extension = filename.split(".")[1]
        identifier=filename.split(".")[0]
        new_path_with_file = os.path.join(IMAGES_FOLDER_OPTIONAL, filename)
        file = Image.open(new_path_with_file)
        width, height = file.size
        side_length = min(width, height)
        left = (width - side_length)/2
        top = (height - side_length)/2
        right = (width + side_length)/2
        bottom = (height + side_length)/2
        image = file.crop((left, top, right, bottom))
        image = image.resize((Crop_size, Crop_size))
        try:
            if (extension.upper() == "JPG"):
                image.save(new_path_with_file, format="JPEG", quality = 100)
            else:
                image.save(new_path_with_file, format=extension.upper())
        finally:
            print('Saved cropped image {}'.format(filename))



print('Done, proceed to training')
