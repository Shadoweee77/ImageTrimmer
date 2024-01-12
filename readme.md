# Image Trimmer

Small program written in Python that aims to trim white space out of images.

The need for this came from scanning a *lot* of family photos. Due to the seemingly random aspect ratio of the old photos, the scanner area doesn't always match and you're left with a white border around the image. There are already several ways to achieve this, such as [Photoshop's automation](https://www.photoshopessentials.com/photo-editing/crop-straighten/) or [ImageMagic script](https://stackoverflow.com/questions/44655961/autotrim-white-border-from-scanned-image-with-imagemagick).

## Deployment
1. Clone the repo using `git clone https://github.com/Shadoweee77/ImageTrimmer.git`.
2. Navigate to the newly created directory
3. Install the requirements using `pip install -r requirements.txt`.

## Usage
Simply run `python main.py` in the ImageTrimmer/ directory. On the first run the program will create 3 directories: `import`, `original` and `export`.
You put the images you want to process into the `import` directory and run the program again. Unedited images are copied to `original` in case something goes wrong. Trimmed images remain in the `export` directory.

## Example
![Example image](https://i.imgur.com/qVJnVVt.jpg)
