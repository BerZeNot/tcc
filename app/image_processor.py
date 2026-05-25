import cv2
import os
import logging
import numpy as np
from cv2.typing import MatLike
from lib.image import image_adjust, apply_gausian_filter, normalize_histogram_spread 

logger = logging.getLogger(__name__)

def load_image(full_path: str): 
    if not os.path.exists(full_path):
        raise FileExistsError("File not exists")

    img = cv2.imread(full_path)
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
    cut_width  = int(np.floor(width  * (percentage / 100)))

    newImg = img[
        cut_height:height - cut_height,
        cut_width:width - cut_width
    ]
    return newImg


def rgb2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# TODO: complete function implementation
def gallus_segseq(imageInGrayScale, filename):
    #function [imseg,thr_im]=gallus_segseq(im,im_file)
    # Autor: Bruno A. N. Travençolo
    # FACOM - UFU
    # Data: 21/07/2010 last update 05/10/2011
    #
    # Segmentar a imagem de espermatozóides


    #uniformizando a imagem
    #im = medfilt2(im,[5 5]);
    #im = imtophat(im,strel('disk',15));
    imageInGrayScale = image_adjust.cv2(imageInGrayScale)

    # smoothing image      
    image_gauss =  apply_gausian_filter(imageInGrayScale,1)
    #im_gauss = im;

    #aumentando o espalhamento do histograma
    im_gauss = normalize_histogram_spread(im_gauss)
    # segmentando a imagem
    im_seg_g = gallus_segment(im_gauss);

    # limpando componentes conexos pequenos

    
    se = strel('disk',1,0);
    im_seg_clean_g = imerode( im_seg_g,se);  
    # im_seg_clean_g =  im_seg_g;  
    
    # colocando uma borda ao redor da imagem para eliminar, por tamanho
    # os espermatozóides de borda
    borda=25
    im_seg_clean_g(1:borda,:) = 1;
    im_seg_clean_g(:,1:borda) = 1;
    im_seg_clean_g(end-borda:end,:) = 1;
    im_seg_clean_g(:,end-borda:end) = 1;
    
    # Parâmetros para limpar os componentes conexos
    maxsize = 70*3*1.15; 
    minsize = 70*2

    im_seg_clean_g = gallus_cleancc(im_seg_clean_g,minsize,maxsize,0)


    # utilizando Erosao/Dilatação para remover a cauda   
    #im_ed_g = bull_erodedilate(im_seg_clean_g);

    # limpando componentes conexos pequenos novamente
    #maxsize = 1*60*60;  # diminuindo o tamanho máximo
    #minsize = 1*30*30;
    #im_ed_g_cleancc = cleancc(im_ed_g,minsize,maxsize);# jah faz o bw_label

    ### salvando os resultados

    write_image(im_gauss/255.0, ['aux_files\\',filename,'_g_gau.png']  )
    write_image(im_seg_g,       ['aux_files\\',filename,'_g_seg.png']  )
    #imwrite(im_seg_clean_g, ['aux_files\\',im_file,'_g_seg_clean.png']  );
    #imwrite(im_ed_g,        ['aux_files\\',im_file,'_g_seg_ed_g.png']);
    #imwrite(im_ed_g_cleancc,        ['aux_files\\',im_file,'_g_seg_clean_ed.png']);
    write_image(im_seg_clean_g,        ['aux_files\\',filename,'_seg.png'])

    #resultado final
    imseg = im_seg_clean_g
    thr_im = im_seg_g

# TODO: complete function implementation
def gallus_segment(image: MatLike):
    return

def write_image(path, img):
    logger.info(f"Writing image in path '{path}'")
    return cv2.imwrite(path, img)