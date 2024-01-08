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

def get_contours(img):
    # Convert the image to grayscale
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get contours
    ret, thresh = cv2.threshold(imgray, 150, 255, 0)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size
    size = get_size(img)
    contours = [cc for cc in contours if contourOK(cc, size)]
    return contours

def get_size(img):
    ih, iw = img.shape[:2]
    return iw * ih

def contourOK(cc, size=1000000):
    x, y, w, h = cv2.boundingRect(cc)
    # Reject contours that are too small or too large
    if w < 50 or h < 50:
        return False
    area = cv2.contourArea(cc)
    return 200 < area < (size * 0.5)

def find_boundaries(img, contours):
    # Initialize boundary variables
    minx, miny, maxx, maxy = img.shape[1], img.shape[0], 0, 0

    # Update boundaries based on contour bounding boxes
    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x + w)
        maxy = max(maxy, y + h)

    return minx, miny, maxx, maxy

def crop(img, boundaries):
    minx, miny, maxx, maxy = boundaries
    return img[miny:maxy, minx:maxx]

def trim_image(file_path):
    img = cv2.imread(file_path)
    contours = get_contours(img)
    bounds = find_boundaries(img, contours)
    cropped = crop(img, bounds)

    # Check if the cropped image is too small
    if get_size(cropped) < 400:
        return None

    return cropped

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
