import json
import os
import timeit

import cv2
import imutils
import numpy as np
import requests
from imutils.object_detection import non_max_suppression
from PIL import Image, ImageEnhance
from skimage.exposure import histogram
from skimage.metrics import structural_similarity as ssim
from tensorflow.python.ops.numpy_ops import np_config

np_config.enable_numpy_behavior()


class ImageEnhancement(object):
    def __init__(self):
        pass

    def __call__(self, image):
        init_dtype = image.dtype

        if np.max(image) <= 1.0:
            print(f"My np.max is low")
            image = (image * 255.0).astype(np.uint8)
        enhanced_image = self.enhance_image(image)

        if init_dtype == np.uint8:
            enhanced_image = (enhanced_image * 255.0).astype(np.uint8)

        return enhanced_image

    @staticmethod
    def enhance_image(image):
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

        image = image.astype(np.float32)
        image = np.clip(image, min_intensity, max_intensity)
        image = (image - min_intensity) / (max_intensity - min_intensity)

        return image


os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf


def unsharp_mask(img, blur_size=(9, 9), imgWeight=1.5, gaussianWeight=-0.5):
    gaussian = cv2.GaussianBlur(img, blur_size, 0)
    return cv2.addWeighted(img, imgWeight, gaussian, gaussianWeight, 0)


# docker run -t --rm -p 8502:8501 -v "C:\Users\maged\Desktop\Projects\PyCharm_Projects\21_Django_ML\algorithms
# \HSV_Model\:/models/HSV_Model/" -e MODEL_NAME=HSV_Model tensorflow/serving &
url_hsv = 'http://tfserving_classifier_hsv:8501/v1/models/model:predict'

# docker run -t --rm -p 8503:8501 -v "C:\Users\maged\Desktop\Projects\PyCharm_Projects\21_Django_ML\algorithms
# \SSIM_Model\:/models/SSIM_Model/" -e MODEL_NAME=SSIM_Model tensorflow/serving &
url_ssim = 'http://tfserving_classifier_ssim:8501/v1/models/model:predict'


def make_prediction_HSV(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url_hsv, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions


def make_prediction_SSIM(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url_ssim, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions


"""
Part 0: Get video from folder
"""
# model_1 = tf.keras.models.load_model("algorithms/capillaryNet")
# model_2 = tf.keras.models.load_model("algorithms/categorical_2class_2")

INPUT_SIZE = (15, 15)
accepted_accuracy = 0.10
true_coords = []
false_coords = []

image_enhancement = ImageEnhancement()

start_time = timeit.default_timer()


def hsv_pipeline(input_frame):
    """
    Part 1: Blur image
    """

    img = cv2.blur(input_frame, (5, 5))
    img = unsharp_mask(img)
    img = unsharp_mask(img)

    """
    Part 2: Enhance Image
    """

    frame_array = Image.fromarray(img)
    enh_col = ImageEnhance.Color(frame_array)
    color = 3
    image_colored = enh_col.enhance(color)

    enh_con = ImageEnhance.Contrast(image_colored)

    contrast = 2.5
    image_contrasted = enh_con.enhance(contrast)
    en_opencvImage_color = np.array(image_contrasted)
    opencvImage_color = en_opencvImage_color.copy()

    """
    Part 3: Convert to HSV
    """

    hsv = cv2.cvtColor(opencvImage_color, cv2.COLOR_BGR2HSV)

    """
    Part 4: Crop HSV colors in range
    """
    mask1 = cv2.inRange(hsv, (155, 60, 0), (180, 255, 255))
    target = cv2.bitwise_and(opencvImage_color, opencvImage_color, mask=mask1)

    """
    Part 5: Grab contours by using OTSU
    """
    target_gray = cv2.cvtColor(target, cv2.COLOR_HSV2BGR)
    target_gray = cv2.cvtColor(target_gray, cv2.COLOR_BGR2GRAY)

    # Get the value of OTSU thresholding
    (T, threshInv) = cv2.threshold(target_gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contour_outline = cv2.findContours(threshInv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    coords = imutils.grab_contours(contour_outline)

    """
    Part 6: Get bounding boxes from threshold calculation
    """

    overlapped_coords_HSV = []
    for i, c in enumerate(coords):
        (x, y, w, h) = cv2.boundingRect(c)

        if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 10000:
            continue

        if cv2.contourArea(c) < 100:
            startX = x - 100
            startY = y - 100
            endX = x + w + 50
            endY = y + h + 50
        else:
            startX = x - 10
            startY = y - 10
            endX = x + w + 10
            endY = y + h + 10

        if startX < 0:
            startX = 0

        if startY < 0:
            startY = 0

        if endX > 1920:
            endX = 1920

        if endY > 1080:
            endY = 1080

        overlapped_coords_HSV.append([startX, startY, endX, endY])

        """
        Part 7: Predict whether it is a capillary or not
        """

        predict_with_deep_learning = True
        if predict_with_deep_learning:
            cv2.rectangle(opencvImage_color, (startX, startY), (endX, endY), (0, 255, 0), 2)

            temp_image = cv2.resize(opencvImage_color[startY:endY, startX:endX], INPUT_SIZE)

            reshaped_array = tf.expand_dims(temp_image, 0)

            predictions = make_prediction_HSV(reshaped_array)

            if predictions[0][0] > accepted_accuracy:
                # cv2.rectangle(input_frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                true_coords.append([startX, startY, endX, endY])

    potential_capillaries_temp_array = np.array(true_coords, dtype=np.float32)
    potential_capillaries_non_max = non_max_suppression(potential_capillaries_temp_array, overlapThresh=0.1)

    return potential_capillaries_non_max, en_opencvImage_color


def ssim_pipeline(original_frame):
    image1_gray = cv2.createBackgroundSubtractorMOG2().apply(original_frame)
    frame_gry = cv2.cvtColor(original_frame, cv2.COLOR_RGB2GRAY)

    # Compute SSIM between two images
    (score, diff) = ssim(image1_gray, frame_gry, win_size=15, multichannel=False, full=True,
                         use_sample_covariance=True)

    diff = (diff * 255).astype("uint8")

    _, segmented_image = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    coords = cv2.findContours(segmented_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    coords = imutils.grab_contours(coords)

    overlapped_coords_SSIM = []
    for c in coords:
        x, y, w, h = cv2.boundingRect(c)

        if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 10000:
            continue

        else:
            startX = x - 50
            startY = y - 50
            endX = x + w + 50
            endY = y + h + 50

            if startX < 0:
                startX = 0

            if startY < 0:
                startY = 0

            if endX > 1920:
                endX = 1920

            if endY > 1080:
                endY = 1080

            overlapped_coords_SSIM.append([startX, startY, endX, endY])

            predict_with_deep_learning = True
            if predict_with_deep_learning:

                cv2.rectangle(original_frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                # Predict here
                temp_image = cv2.resize(original_frame[startY:endY, startX:endX], (50, 50))
                temp_image_enhanced = image_enhancement(temp_image)

                # Take the below lines out and added to Ray Serve and ping it
                reshaped_array = tf.expand_dims(temp_image_enhanced, 0)

                predictions = make_prediction_SSIM(reshaped_array)

                if predictions[0][1] > accepted_accuracy:
                    true_coords.append([startX, startY, endX, endY])
                    # cv2.rectangle(original_frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    potential_capillaries_temp_array = np.array(true_coords, dtype=np.float32)
    potential_capillaries_non_max = non_max_suppression(potential_capillaries_temp_array, overlapThresh=0.1)

    return potential_capillaries_non_max


def combine_images(enhanced_hsv_image, capillary_coords):
    capillary_coords_compressed = non_max_suppression(capillary_coords, overlapThresh=0.1)

    for coords in capillary_coords_compressed:
        cv2.rectangle(enhanced_hsv_image, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)

    return enhanced_hsv_image


def classify_image_using_algorithm_v2(image_api):
    start_time = timeit.default_timer()
    image_from_frontend = cv2.imread(image_api)
    capillaries_hsv_coords, hsv_enhanced_image = hsv_pipeline(image_from_frontend)
    capillaries_ssim_coords = ssim_pipeline(image_from_frontend)
    final_image = combine_images(hsv_enhanced_image, np.concatenate((capillaries_hsv_coords, capillaries_ssim_coords)))

    time_taken = str(round(timeit.default_timer() - start_time, 2)) + " seconds"

    return time_taken, Image.fromarray(final_image)


"""
Part 8: Display results
"""

if __name__ == "__main__":
    original_image = cv2.imread("testSample.png")

    hsv_coords, hsv_image = hsv_pipeline(original_image)
    ssim_coords = ssim_pipeline(original_image)
    final = combine_images(hsv_image, np.concatenate((hsv_coords, ssim_coords)))

    cv2.imshow("final_image", final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
