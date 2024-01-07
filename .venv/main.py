import shutil
import numpy as np
import cv2
import os

def is_border_white(binary_image, border_size=1):
    # Get the border region
    top_border = binary_image[:border_size, :]  # Top border
    bottom_border = binary_image[-border_size:, :]  # Bottom border
    left_border = binary_image[:, :border_size]  # Left border
    right_border = binary_image[:, -border_size:]  # Right border

    # Concatenate the border regions
    border_regions = [top_border, bottom_border, left_border, right_border]

    # Check if any pixel values in the border regions are non-zero
    return not np.any([np.any(border) for border in border_regions])

def trim_image(img_path):
    img = cv2.imread(img_path)
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)
        edges = cv2.Canny(blur, 50, 150)

        # Convert the edge-detected image to binary
        _, binary_image = cv2.threshold(edges, 1, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_contour = max(contours, key=len)

        # Calculate bounding box around max_contour
        x, y, w, h = cv2.boundingRect(max_contour)

        # Extend bounding box by 5%
        margin_percentage = 0.005
        margin_x = int(w * margin_percentage)
        margin_y = int(h * margin_percentage)

        x -= margin_x
        y -= margin_y
        w += 2 * margin_x
        h += 2 * margin_y

        # Ensure the coordinates are within the image bounds
        x = max(0, x)
        y = max(0, y)
        w = min(img.shape[1] - x, w)
        h = min(img.shape[0] - y, h)

        # Trim the image to the calculated bounding box
        trimmed_image = img[y:y+h, x:x+w]

        # Check if the border around the trimmed region is white or close to white
        if is_border_white(binary_image):
            return trimmed_image
        else:
            print("Error: Border around the trimmed region is not white or close to white.")
            return None
    else:
        print("Error: Unable to read image at path:", img_path)
        return None


def main():
    import_path = os.path.join(os.getcwd(), 'import')
    original_path = os.path.join(os.getcwd(), 'original')
    export_path = os.path.join(os.getcwd(), 'export')

    for file in os.listdir(import_path):
        if file.endswith('.jpg') or file.endswith('.png'):
            print("Cloning image to \\original\\:", file)
            try:
                shutil.copy(os.path.join(import_path, file), os.path.join(original_path, file))
                print("Image cloned")
                try:
                    print("Processing image:", file)
                    trimmed_image = trim_image(os.path.join(original_path, file))
                    if trimmed_image is not None:
                        cv2.imshow("Trimmed Image", trimmed_image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()

                        try:
                            cv2.imwrite(os.path.join(export_path, file), trimmed_image)
                            os.remove(os.path.join(import_path, file))
                        except OSError as e:
                            print("Error writing image:", e)

                    else:
                        print("Something went wrong.")
                except OSError as e:
                    print("Error processing image:", e)

            except Exception as e:
                print("Error copying:", e)

if __name__ == "__main__":
    main()
