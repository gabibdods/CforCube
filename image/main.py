import sys
import cv2 as cv
import numpy as np

def save_image(path, image):
    cv.imwrite(path, image)

def downsize_image(image):
    return cv.resize(image, None, fx=0.5, fy=0.5)

def load_image(path):
    if path == "skip":
        return None
    if cv.imread(path) is None:
        print("\nUnresolvable path. Exiting gracefully.\n")
        sys.exit(0)
    return cv.imread(path)

def silence(filtr):
    antinoise = np.ones((20, 20), np.uint8)
    highlight = cv.morphologyEx(filtr, cv.MORPH_OPEN, antinoise)
    highlight = cv.morphologyEx(highlight, cv.MORPH_CLOSE, antinoise)
    return highlight

def draw_contour(highlight, image):
    contours, _ = cv.findContours(highlight, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area < 1000:
            continue
        perimeter = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.05 * perimeter, True)

        if len(approx) == 4:
            x, y, w, h = cv.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 0.8 <= aspect_ratio <= 1.2:
                cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 40), 2)
    return image

def create_test_window(image, preset):
    def nothing(x):
        pass
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    cv.namedWindow("Test", cv.WINDOW_NORMAL)
    cv.createTrackbar("H_min", "Test", preset[0][0], 179, nothing)
    cv.createTrackbar("S_min", "Test", preset[0][1], 255, nothing)
    cv.createTrackbar("V_min", "Test", preset[0][2], 255, nothing)
    cv.createTrackbar("H_max", "Test", preset[1][0], 179, nothing)
    cv.createTrackbar("S_max", "Test", preset[1][1], 255, nothing)
    cv.createTrackbar("V_max", "Test", preset[1][2], 255, nothing)
    while True:
        try:
            h_min = cv.getTrackbarPos("H_min", "Test")
            s_min = cv.getTrackbarPos("S_min", "Test")
            v_min = cv.getTrackbarPos("V_min", "Test")
            h_max = cv.getTrackbarPos("H_max", "Test")
            s_max = cv.getTrackbarPos("S_max", "Test")
            v_max = cv.getTrackbarPos("V_max", "Test")
        except cv.error:
            print("\nWindow closed. Exiting gracefully.\n")
            sys.exit(0)
        darker = np.array([h_min, s_min, v_min])
        lighter = np.array([h_max, s_max, v_max])
        edit = cv.inRange(image, darker, lighter)
        product = cv.bitwise_and(image, image, mask=edit)
        final = cv.cvtColor(product, cv.COLOR_HSV2BGR)
        cv.imshow("Test", final)
        if cv.waitKey(1) & 0xFF == 27:
            break
    cv.destroyAllWindows()

def create_showcase_window(img, low, high):
    if img is None:
        print("\nEmpty image. Exiting gracefully.\n")
        sys.exit(0)
    image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(image, low, high)
    silenced = silence(mask)
    highlighted = cv.bitwise_and(image, image, mask=silenced)
    gridded = draw_contour(silenced, highlighted)

    show = cv.cvtColor(gridded, cv.COLOR_HSV2BGR)
    cv.imshow("Face", downsize_image(show))
    cv.waitKey(0)
    cv.destroyAllWindows()

def mask_main(f2i, f2m, f2mr):
    i = input("blue || green || orange || red || white || yellow || rainbow ?\n")
    if i == "rainbow":
        p = f2mr[input("blue || green || orange || red || white || yellow || default ?\n")]
    else:
        p = f2m[i] if input("masked?\n") == "" else f2m["default"]
    create_test_window(f2i[i], p)

def test_main(f2i, f2m):
    for face, (lo, hi) in f2m.items():
        create_showcase_window(f2i[face], lo, hi)

def show_main(f2mr):
    for face, (lo, hi) in f2mr.items():
        create_showcase_window(load_image(r".\rainbow.jpg"), lo, hi)

def main():
    faces_to_images =\
    {
        "blue": load_image(r".\blu.jpg"),
        "green": load_image(r".\verde.jpg"),
        "orange": load_image(r".\arancione.jpg"),
        "red": load_image(r".\rosso.jpg"),
        "white": load_image(r".\bianco.jpg"),
        "yellow": load_image(r".\giallo.jpg"),
        "rainbow" : load_image(r".\rainbow.jpg"),
        "default" : load_image("skip")
    }
    faces_to_masks =\
    {
        "blue": (np.array([94, 44, 94]), np.array([109, 215, 218])),
        "green": (np.array([46, 44, 108]), np.array([75, 211, 255])),
        "orange": (np.array([2, 44, 133]), np.array([15, 255, 255])),
        "red": (np.array([0, 58, 207]), np.array([179, 205, 255])),
        "white": (np.array([0, 0, 178]), np.array([117, 14, 255])),
        "yellow": (np.array([30, 68, 100]), np.array([44, 255, 255])),
        "default" : (np.array([0, 0, 0]), np.array([255, 255, 255]))
    }
    faces_to_masks_rainbow =\
    {
        "blue": (np.array([104, 66, 107]), np.array([130, 255, 255])),
        "green": (np.array([43, 79, 64]), np.array([80, 211, 255])),
        "orange": (np.array([10, 118, 150]), np.array([18, 255, 255])),
        "red": (np.array([0, 118, 150]), np.array([4, 255, 255])),
        "white": (np.array([0, 0, 237]), np.array([168, 7, 255])),
        "yellow": (np.array([17, 67, 235]), np.array([168, 255, 255])),
        "default" : (np.array([0, 0, 0]), np.array([255, 255, 255]))
    }
    choice = input("mask || test || show ?\n")
    if choice == "mask":
        mask_main(faces_to_images, faces_to_masks, faces_to_masks_rainbow)
    elif choice == "test":
        test_main(faces_to_images, faces_to_masks)
    elif choice == "show":
        show_main(faces_to_masks_rainbow)

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    return cv.warpAffine(image, cv.getRotationMatrix2D((w // 2, h // 2), angle, 1.0), (w, h))

def blur_image(image, kernel_size):
    return cv.GaussianBlur(image, (kernel_size, kernel_size), 0)

if __name__ == "__main__":
    main()

#PS> python -m venv .venv
#PS> .venv\Scripts\activate
#PS> pip install opencv-python nympy pillow matplotlib
#PS> python main.py