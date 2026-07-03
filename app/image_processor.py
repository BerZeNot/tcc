import cv2
import os
import logging
import numpy as np
from cv2.typing import MatLike
from lib.image import image_adjust, apply_gausian_filter, normalize_histogram_spread
from lib.gallus_segment import gallus_segment
from lib.gallus_clean_cc import gallus_clean_cc

logger = logging.getLogger(__name__)


def load_image(full_path: str, convert2grayscale=False):
    if not os.path.exists(full_path):
        raise FileExistsError("File not exists")

    img = cv2.imread(full_path)
    if convert2grayscale:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return assert_rgb_image(img)


# Asserts that the img is RGB:
# if is grayscale, converts to RGB
# else returns the original image
def assert_rgb_image(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        return img
    return img


# Cut image edges in percentage%
def cut_edges(img, percentage):
    height, width = img.shape[:2]

    cut_height = int(np.floor(height * (percentage / 100)))
    cut_width = int(np.floor(width * (percentage / 100)))

    newImg = img[cut_height : height - cut_height, cut_width : width - cut_width]
    return newImg


def invert_image(image: MatLike):
    return np.uint8((image < 127) * 255)


def rgb2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def gallus_segseq(imageInGrayScale, filename, aux_files_path):

    imageInGrayScale = image_adjust(imageInGrayScale)

    # smoothing image
    image_gauss = apply_gausian_filter(imageInGrayScale, 1)

    # aumentando o espalhamento do histograma
    image_gauss = normalize_histogram_spread(image_gauss)

    # segmentando a imagem
    im_seg_g, _ = gallus_segment(image_gauss)

    # limpando componentes conexos pequenos
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    im_seg_clean_g = cv2.erode(im_seg_g.astype(np.uint8), se)

    # colocando uma borda ao redor da imagem para eliminar, por tamanho
    # os espermatozóides de borda
    borda = 25

    im_seg_clean_g[:borda, :] = 1
    im_seg_clean_g[:, :borda] = 1
    im_seg_clean_g[-borda:, :] = 1
    im_seg_clean_g[:, -borda:] = 1

    # Parâmetros para limpar os componentes conexos
    maxsize = 70 * 3 * 1.15
    minsize = 70 * 2

    im_seg_clean_g = gallus_clean_cc(im_seg_clean_g, minsize, maxsize, 0)

    ## salvando os resultados
    write_image(f"{aux_files_path}/{filename}_g_gau.png", image_gauss)
    write_image(f"{aux_files_path}/{filename}_g_seg.png", im_seg_g)
    write_image(f"{aux_files_path}/{filename}_seg.png", im_seg_clean_g)

    # resultado final
    imseg = im_seg_clean_g
    thr_im = im_seg_g
    return imseg, thr_im


def write_image(path, img):
    logger.info(f"Writing image in path '{path}'")

    if img.dtype != np.uint8:
        img = np.clip(img * 255, 0, 255).astype(np.uint8)

    return cv2.imwrite(path, img)
