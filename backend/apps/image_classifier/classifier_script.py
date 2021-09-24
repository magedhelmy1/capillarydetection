import cv2
from PIL import ImageEnhance
import imutils
import numpy as np
from skimage.exposure import histogram
from skimage import color
from PIL import Image
import timeit


class ImageEnhancement(object):
    def __init__(self, modify_color=True):
        self.modify_color = modify_color

    def __call__(self, image):
        init_dtype = image.dtype

        if np.max(image) <= 1.0:
            image = (image * 255.0).astype(np.uint8)
        enhanced_image = self.enhance_image(image, modify_color=self.modify_color)

        if init_dtype == np.uint8:
            enhanced_image = (enhanced_image * 255.0).astype(np.uint8)

        return enhanced_image

    def enhance_image(self, image, modify_color: bool, verbose=False):
        # Calculate intensity histogram
        hist, hist_centers = histogram(image)

        # Find min intensity
        percentage_to_drop = 0.01
        nr_of_pixels = image.shape[0] * image.shape[1]
        min_intensity = 0
        max_intensity = 255
        for i in range(1, len(hist)):  # Skip zero intensity pixels
            if hist[i] > nr_of_pixels * percentage_to_drop:
                min_intensity = hist_centers[i]
                break

        # Find end intensity
        for i in range(len(hist) - 1, 0, -1):
            if hist[i] > nr_of_pixels * percentage_to_drop:
                max_intensity = hist_centers[i]
                break

        if verbose:
            print('min/max intensity:', min_intensity, max_intensity)

        image = image.astype(np.float32)
        image = np.clip(image, min_intensity, max_intensity)
        image = (image - min_intensity) / (max_intensity - min_intensity)

        if modify_color:
            image = color.rgb2hsv(image)

            # Boost reds
            selection = np.any([image[:, :, 0] < 0.05, image[:, :, 0] > 0.95], axis=0)
            image[selection, 1] = np.power(image[selection, 1], 0.9)

            # Reduce other
            selection = np.all([image[:, :, 0] > 0.1, image[:, :, 0] < 0.8], axis=0)
            image[selection, 1] = np.power(image[selection, 1], 1.2)

            image = color.hsv2rgb(image)

        return image


def enhance_image(img_orig):
    frame_en = Image.fromarray(img_orig)
    enh_col = ImageEnhance.Color(frame_en)
    color = 1.5

    image_en = enh_col.enhance(color)
    enh_con = ImageEnhance.Contrast(image_en)

    contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    img_contrasted = np.array(image_contrasted)

    return img_contrasted


def extract_frame_from_video(video_dir, frame_number):
    print(f" Video Name: {video_path}")
    capture = cv2.VideoCapture(video_path)

    counter = 0
    while True:
        ret, frame = capture.read()

        if counter == frame_number:
            image = cv2.imwrite("frame.png", frame)
            break

        counter += 1

    return frame


def return_channel(frame_multi):
    b, g, r = cv2.split(frame_multi)

    return g


def denoise_frame(noisy_frame):
    return cv2.fastNlMeansDenoising(noisy_frame, None, 11, 11, 21)


def segment_background(img_unseg, frame_to_blend_with):
    thresh1 = cv2.adaptiveThreshold(img_unseg, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY_INV, 199, 10)
    original_masked = cv2.bitwise_and(frame_to_blend_with, frame_to_blend_with, mask=thresh1)

    return original_masked


def remove_high_green_pixels(masked_image):
    masked_image_copy = masked_image.copy()

    green_value = masked_image_copy[:, :, 1]
    red_value = masked_image_copy[:, :, 2]
    q = green_value > red_value

    masked_image_copy[q] = [0, 0, 0]
    #
    # hsv = cv2.cvtColor(masked_image_copy, cv2.COLOR_BGR2HSV)
    # q = hsv[..., 1] < 90
    # masked_image_copy[q] = [0, 0, 0]

    # masked_image_copy = cv2.cvtColor(masked_image_copy, cv2.COLOR_HSV2BGR)

    return masked_image_copy


def get_countours_apply_to_image(res_img, image_to_write_on):
    res_gray = cv2.cvtColor(res_img, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(res_gray.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for i, c in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)

        if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 30000:
            continue

        startX = x - 20
        startY = y - 20
        endX = x + w + 20
        endY = y + h + 20

        if startX < 0:
            startX = 0

        if startY < 0:
            startY = 0

        if endX > 1920:
            endX = 1920

        if endY > 1080:
            endY = 1080

        cv2.rectangle(image_to_write_on, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return image_to_write_on


def classify_image(frame):
    img_temp = Image.open(frame)
    frame_ready = cv2.cvtColor(np.array(img_temp), cv2.COLOR_RGB2BGR)

    start_time = timeit.default_timer()

    image_enhancement = ImageEnhancement(modify_color=False)
    org_enhanced = image_enhancement(frame_ready)

    # load channel
    g = return_channel(frame_ready)

    # denoise frame
    denoised_img = denoise_frame(g)

    # apply contours to image
    segmented_bg = segment_background(denoised_img, org_enhanced)

    cleaned_img = remove_high_green_pixels(segmented_bg)

    img = get_countours_apply_to_image(cleaned_img, org_enhanced)
    im_pil = Image.fromarray(img)

    time_taken = timeit.default_timer() - start_time

    return time_taken, im_pil


if __name__ == "__main__":
    pass
