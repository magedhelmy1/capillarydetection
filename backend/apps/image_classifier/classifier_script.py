import timeit
import tensorflow as tf
import imutils
import numpy as np
from skimage.exposure import histogram
from skimage import color
import os
import cv2
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim

# Use CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class ImageEnhancement(object):
    def __init__(self, modify_color=True):
        self.modify_color = modify_color

    def __call__(self, image):
        init_dtype = image.dtype

        if np.max(image) <= 1.0:
            image = (image * 255.0).astype(np.uint8)
        enhanced_image = enhance_image(image, modify_color=self.modify_color)

        if init_dtype == np.uint8:
            enhanced_image = (enhanced_image * 255.0).astype(np.uint8)

        return enhanced_image


def enhance_image(image, modify_color: bool, verbose=False):
    # Calculate intensity histogram
    hist, hist_centers = histogram(image)

    # Plot histogram
    # plt.plot(hist_centers, hist)
    # plt.show()

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
    image = np.divide((image - min_intensity), (max_intensity - min_intensity))

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


def unsharp_mask(img, blur_size=(9, 9), imgWeight=1.5, gaussianWeight=-0.5):
    gaussian = cv2.GaussianBlur(img, blur_size, 0)
    return cv2.addWeighted(img, imgWeight, gaussian, gaussianWeight, 0)


def classify_image(image_to_read):
    start_time = timeit.default_timer()

    image_enhancement = ImageEnhancement(modify_color=False)

    model = tf.keras.models.load_model("algorithms/capillaryNet")
    model_2 = tf.keras.models.load_model("algorithms/categorical_2class_2")
    INPUT_SIZE = (15, 15)
    accepted_accuracy = 0.90
    true_coords = []
    false_coords = []

    img = Image.open(image_to_read)
    opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    HSV = True
    if HSV == True:
        cv2_image = opencvImage

        """
        Part 1: Blur image
        """

        start_time = timeit.default_timer()

        img = cv2.blur(cv2_image, (5, 5))
        img = unsharp_mask(img)
        img = unsharp_mask(img)

        """
        Part 2: Enhance Image
        """

        frame = Image.fromarray(img)
        enh_col = ImageEnhance.Color(frame)
        color = 2.5
        image_colored = enh_col.enhance(color)

        enh_con = ImageEnhance.Contrast(image_colored)

        contrast = 2.5
        image_contrasted = enh_con.enhance(contrast)
        opencvImage_color = np.array(image_contrasted)

        """
        Part 3: Convert to HSV
        """

        hsv = cv2.cvtColor(opencvImage_color, cv2.COLOR_BGR2HSV)

        """
        Part 4: Crop HSV colors in range
        """

        mask1 = cv2.inRange(hsv, (150, 50, 0), (180, 255, 255))
        target = cv2.bitwise_and(opencvImage_color, opencvImage_color, mask=mask1)

        """
        Part 5: Grab contours by using OTSU
        """
        target_gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)

        # Get the value of OTSU thresholding
        (T, threshInv) = cv2.threshold(target_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contour_outline = cv2.findContours(threshInv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(contour_outline)

        """
        Part 6: Get bounding boxes from threshold calculation
        """
        for i, c in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)

            if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 50000:
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

            """
            Part 7: Predict whether it is a capillary or not
            """

            temp_image = cv2.resize(opencvImage_color[startY:endY, startX:endX], INPUT_SIZE)

            reshaped_array = tf.expand_dims(temp_image, 0)

            predictions = model.predict(reshaped_array)

            if predictions.tolist()[0][0] > accepted_accuracy:
                true_coords.append([startX, startY, endX, endY])
                cv2.rectangle(opencvImage_color, (x, y), (x + w, y + h), (0, 255, 0), 2)


            else:
                false_coords.append([startX, startY, endX, endY])
                # cv2.rectangle(opencvImage_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

    SSIM = True
    if SSIM == True:
        if SSIM:

            image1_gray = cv2.createBackgroundSubtractorMOG2().apply(cv2_image)
            frame_gry = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2GRAY)

            # Compute SSIM between two images
            (score, diff) = ssim(image1_gray, frame_gry, win_size=11, multichannel=False, full=True,
                                 use_sample_covariance=True)

            diff = (diff * 255).astype("uint8")

            _, segmented_image = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            coords = cv2.findContours(segmented_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            coords = imutils.grab_contours(coords)

            for c in coords:
                x, y, w, h = cv2.boundingRect(c)

                if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 1000:
                    continue

                else:
                    startX = x - 10
                    startY = y - 10
                    endX = x + w + 10
                    endY = y + h + 10

                    if startX < 0:
                        startX = 0

                    if startY < 0:
                        startY = 0

                    # when not clipping corners
                    if endX > 1920:
                        endX = 1920

                    if endY > 1080:
                        endY = 1080

                    # Predict here
                    temp_image = cv2.resize(cv2_image[startY:endY, startX:endX], (50, 50))
                    temp_image_enhanced = image_enhancement(temp_image)

                    # Take the below lines out and added to Ray Serve and ping it
                    reshaped_array = tf.expand_dims(temp_image_enhanced, 0)

                    prediction = model_2.predict(reshaped_array)

                    if prediction.tolist()[0][1] > 0.9:
                        true_coords.append([startX, startY, endX, endY])
                        cv2.rectangle(opencvImage, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    else:
                        false_coords.append([startX, startY, endX, endY])
                        # cv2.rectangle(opencvImage_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

    """
    Part 8: Display results
    """

    time_taken = timeit.default_timer() - start_time

    img = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)


    return time_taken, im_pil


if __name__ == "__main__":
    pass
