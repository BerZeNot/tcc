import cv2
import os
import logging
import numpy as np
from cv2.typing import MatLike
from lib.image import image_adjust, apply_gausian_filter, normalize_histogram_spread
from lib.gallus_segment import gallus_segment
from lib.gallus_clean_cc import gallus_clean_cc
from lib.bull_erode_dilate import bull_erodedilate

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


def bull_segseq(image_in_gray_scale, filename, aux_files_path):
    # smoothing image
    image_gauss = apply_gausian_filter(image_in_gray_scale, 1)

    # segmentando a imagem
    image_gauss_seg, _ = gallus_segment(image_gauss)

    # limpando componentes conexos pequenos
    maxsize = 100 * 150
    minsize = 10

    image_gauss_seg_cleancc = gallus_clean_cc(
        image_gauss_seg,
        minsize,
        maxsize,
        1,
    )

    # utilizando erosão/dilatação para remover a cauda
    image_gauss_seg_cleancc_erodedilate = bull_erodedilate(
        image_gauss_seg_cleancc,
        2,
    )

    # limpando componentes conexos pequenos novamente
    maxsize = 130 * 80
    minsize = maxsize / 5

    image_gauss_seg_cleancc_erodedilate_cleancc = gallus_clean_cc(
        image_gauss_seg_cleancc_erodedilate,
        minsize,
        maxsize,
    )

    image_gauss_seg_cleancc_erodedilate_cleancc_closing = (
        image_gauss_seg_cleancc_erodedilate_cleancc
    )

    # salvando os resultados
    write_image(
        f"{aux_files_path}/{filename}_01_gauss_tmp.png",
        image_gauss / 255.0,
    )

    write_image(
        f"{aux_files_path}/{filename}_02_gauss_seg_tmp.png",
        image_gauss_seg,
    )

    write_image(
        f"{aux_files_path}/{filename}_03_gauss_seg_cleancc_tmp.png",
        image_gauss_seg_cleancc,
    )

    write_image(
        f"{aux_files_path}/{filename}_04_gauss_seg_cleancc_erodedilate_tmp.png",
        image_gauss_seg_cleancc_erodedilate,
    )

    write_image(
        f"{aux_files_path}/{filename}_05_gauss_seg_cleancc_erodedilate_cleancc_tmp.png",
        image_gauss_seg_cleancc_erodedilate_cleancc,
    )

    write_image(
        f"{aux_files_path}/{filename}_06_gauss_seg_cleancc_erodedilate_cleancc_closing_tmp.png",
        image_gauss_seg_cleancc_erodedilate_cleancc_closing,
    )

    # resultado final
    imseg = image_gauss_seg_cleancc_erodedilate_cleancc_closing
    thr_im = image_gauss_seg

    write_image(
        f"{aux_files_path}/{filename}_seg.png",
        imseg,
    )

    return imseg, thr_im


def write_image(path, img):
    logger.info(f"Writing image in path '{path}'")

    if img.dtype != np.uint8:
        img = np.clip(img * 255, 0, 255).astype(np.uint8)

    return cv2.imwrite(path, img)
