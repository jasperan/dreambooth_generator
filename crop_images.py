import shutil
from PIL import Image
import os

Remove_existing_instance_images= False


if Remove_existing_instance_images:
  if os.path.exists(str(INSTANCE_DIR)):
    !rm -r "$INSTANCE_DIR"

if not os.path.exists(str(INSTANCE_DIR)):
  %mkdir -p "$INSTANCE_DIR"

IMAGES_FOLDER_OPTIONAL="/home/ubuntu/dreambooth_nacho" #@param{type: 'string'}


Crop_images= True
Crop_size = "512"
Crop_size=int(Crop_size)


while IMAGES_FOLDER_OPTIONAL !="" and not os.path.exists(str(IMAGES_FOLDER_OPTIONAL)):
  print('[1;31mThe image folder specified does not exist, use the colab file explorer to copy the path :')
  IMAGES_FOLDER_OPTIONAL=input('')

if IMAGES_FOLDER_OPTIONAL!="":
  with capture.capture_output() as cap:
    if Crop_images:
      for filename in os.listdir(IMAGES_FOLDER_OPTIONAL):
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
        if (extension.upper() == "JPG"):
            image.save(new_path_with_file, format="JPEG", quality = 100)
        else:
            image.save(new_path_with_file, format=extension.upper())
        %cp -r "$IMAGES_FOLDER_OPTIONAL/." "$INSTANCE_DIR"
        clear_output()      
    else:
      %cp -r "$IMAGES_FOLDER_OPTIONAL/." "$INSTANCE_DIR"

    %cd "$INSTANCE_DIR"
    !find . -name "* *" -type f | rename 's/ /-/g'
    %cd /content
    if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
      %rm -r INSTANCE_DIR+"/.ipynb_checkpoints"      
  print('[1;32mDone, proceed to the training cell')


elif IMAGES_FOLDER_OPTIONAL =="":
  uploaded = files.upload()
  if Crop_images:
    for filename in uploaded.keys():
      shutil.move(filename, INSTANCE_DIR)
      extension = filename.split(".")[1]
      identifier=filename.split(".")[0]
      new_path_with_file = os.path.join(INSTANCE_DIR, filename)
      file = Image.open(new_path_with_file)
      width, height = file.size
      side_length = min(width, height)
      left = (width - side_length)/2
      top = (height - side_length)/2
      right = (width + side_length)/2
      bottom = (height + side_length)/2
      image = file.crop((left, top, right, bottom))
      image = image.resize((Crop_size, Crop_size))
      if (extension.upper() == "JPG"):
          image.save(new_path_with_file, format="JPEG", quality = 100)
      else:
          image.save(new_path_with_file, format=extension.upper())
      clear_output()
  else:
    for filename in uploaded.keys():
      shutil.move(filename, INSTANCE_DIR)
      clear_output()

  with capture.capture_output() as cap:
    %cd "$INSTANCE_DIR"
    !find . -name "* *" -type f | rename 's/ /-/g'
    %cd /content
    if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
      %rm -r INSTANCE_DIR+"/.ipynb_checkpoints"
  print('[1;32mDone, proceed to the training cell')

with capture.capture_output() as cap:
  %cd $SESSION_DIR
  !rm instance_images.zip
  !zip -r instance_images instance_images
  %cd /content