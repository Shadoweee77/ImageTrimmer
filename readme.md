
# Image Trimmer

Small program written in Python that aims to trim white spaces out of images.

Need for this progam came from scanning a *lot* of family pictures. Due to the old photos random format the scanner area doesn't always match and You're left with white border around the image. There are different ways to achive this, like [Photoshop's automation](https://www.photoshopessentials.com/photo-editing/crop-straighten/) or [ImageMagic script](https://stackoverflow.com/questions/44655961/autotrim-white-border-from-scanned-image-with-imagemagick).

## Deployment
1. Clone the repo via `git clone https://github.com/Shadoweee77/ImageTrimmer.git`
2. Navigate to the newly created directory
3. Install requirements via `pip install -r requirements.txt`

## Usage
Just run `python main.py` in the ImageTrimmer/ directory. On the initial execution program will create 3 directories: `import`, `original` and `export`.
You input the images to process to the `import` directory and execute the program again. Non modified images will be copied over to `original` just in case something goes wrong. Trimmed images rest in `export` directory.

## Example
![Example image](https://i.imgur.com/qVJnVVt.jpg)