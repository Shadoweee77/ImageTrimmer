import os
import shutil
import numpy as np
import cv2

# ANSI escape codes for colored console output
RESET = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'

def create_folders(*folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"{GREEN}Created folder:{RESET} {folder}")
        else:
            print(f"{YELLOW}Folder already exists:{RESET} {folder}")


def trim_image(image):
    img = cv2.imread(image)
    img = img[:-20, :-20]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 * (gray < 128).astype(np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones((4, 4), dtype=np.uint8))
    coords = cv2.findNonZero(gray)
    x, y, w, h = cv2.boundingRect(coords)
    rect = img[y:y + h, x:x + w]

    return rect


def main():
    # Define folder paths
    import_path = os.path.join(os.getcwd(), 'import')
    original_path = os.path.join(os.getcwd(), 'original')
    export_path = os.path.join(os.getcwd(), 'export')

    # Create necessary folders if they don't exist
    create_folders(import_path, original_path, export_path)

    # Process each image in the import folder
    for file in os.listdir(import_path):
        if file.endswith('.jpg') or file.endswith('.png'):
            print(f"{CYAN}Processing image:{RESET} {file}")
            try:
                # Copy the original image to the original folder
                shutil.copy(os.path.join(import_path, file), os.path.join(original_path, file))
                print(f"{GREEN}Image cloned:{RESET} {file}")

                try:
                    # Trim the image and export if successful
                    trimmed_image = trim_image(os.path.join(original_path, file))
                    if trimmed_image is not None:
                        try:
                            cv2.imwrite(os.path.join(export_path, file), trimmed_image)
                            os.remove(os.path.join(import_path, file))
                            print(f"{GREEN}Image exported:{RESET} {file}")
                        except OSError as e:
                            print(f"{RED}Error writing image:{RESET} {e}")
                    else:
                        print(f"{YELLOW}Image too small, not exported.{RESET}")

                except OSError as e:
                    print(f"{RED}Error processing image:{RESET} {e}")

            except Exception as e:
                print(f"{RED}Error copying:{RESET} {e}")

if __name__ == "__main__":
    main()
