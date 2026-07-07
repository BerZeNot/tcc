import cv2
import numpy as np
from lib.getbb import getbb
from lib.PCAxy import PCAxy
from lib.perim import perim
from lib.entropy import entropy
from textwrap import dedent
import os.path as path


def gallus_sep_heads(imo, im_seg, im_file, print_image, base_folder_path):
    n_ids, bw_im = cv2.connectedComponents(im_seg, connectivity=4)
    imo_selected = imo
    res = []

    valid_id = 0
    for ind_id in range(1, n_ids):

        basefilenamehead = f"{im_file}_h{valid_id}"
        basefilename = path.join("heads", basefilenamehead)

        imbb_seg, original_index, origin = getbb(bw_im, ind_id, 1, True)
        imbb = np.zeros((*imbb_seg.shape, 3), dtype=np.uint8)

        temp = imo[original_index]

        # head coordinates and matrix indexes
        im_x, im_y = np.where(imbb_seg > 0)
        im_index = (im_x, im_y)

        imbb[im_index] = temp

        # TODO: Chances extremamente altas dessas duas variáveis e chamada para PCAxy serem
        # completamente inúteis nesse contexto (remover se for o caso)
        aVal, aVec = PCAxy(im_x, im_y)

        head_skeleton = f"{basefilename}_Skeleton.png"

        SK_imbb_seg = cv2.ximgproc.thinning((imbb_seg > 0).astype(np.uint8) * 255)

        skelength = np.count_nonzero(SK_imbb_seg)

        nbranches = 0

        nendpoints = 0

        # Measurements

        # center of mass
        im_xm = np.mean(im_x)
        im_ym = np.mean(im_y)
        cmass = np.asarray([im_xm, im_ym])

        # area, perimeter
        area = im_x.size

        p = perim(imbb_seg)

        bending = 0

        lab = cv2.cvtColor(imbb, cv2.COLOR_RGB2LAB)

        LAB_l = lab[:, :, 0].astype(np.float64)
        LAB_a = lab[:, :, 1].astype(np.float64) - 128
        LAB_b = lab[:, :, 2].astype(np.float64) - 128

        # mean gray pixels values
        pix_mean = np.mean(LAB_l[im_index])

        # texture
        t = np.std(LAB_l[im_index])

        # entropy
        h = entropy(LAB_l[im_index], 255)

        blue_index = 0

        valid = 1

        if valid:
            if print_image:
                cv2.imwrite(path.join(base_folder_path, head_skeleton), SK_imbb_seg)

            head_seg_fn = f"{basefilename}_seg.bmp"
            head_ori_fn = f"{basefilename}_ori.bmp"

            if print_image:
                cv2.imwrite(path.join(base_folder_path, head_ori_fn), imbb)
                cv2.imwrite(
                    path.join(base_folder_path, head_seg_fn),
                    imbb_seg.astype(np.uint8) * 255,
                )

            head_gray_fn = f"{basefilename}_Gray.png"

            if print_image:
                cv2.imwrite(
                    path.join(base_folder_path, head_gray_fn), LAB_l.astype(np.uint8)
                )

            imo_selected[original_index] = [0, 0, 255]

            write_in_html(
                base_folder_path,
                basefilename,
                valid_id,
                im_file,
                valid,
                basefilenamehead,
                t,
                area,
                p,
                h,
                blue_index,
                pix_mean,
                nendpoints,
                nbranches,
                skelength,
                bending,
            )

            resh = [
                valid_id,
                valid,
                area,
                p,
                t,
                h,
                blue_index,
                pix_mean,
                nendpoints,
                nbranches,
                skelength,
                bending,
            ]

            res.append(resh)
            np.savetxt(
                path.join(base_folder_path, f"{basefilename}.txt"),
                np.asarray(resh).reshape(1, -1),
                fmt="%.10f",
            )

            valid_id += 1
    res_colname = [
        "id",
        "Valid",
        "Area",
        "Perimeter",
        "Texture",
        "Entropy",
        "Blue index",
        "Mean pixel value (grayscale)",
        "NEndPoints",
        "NBranches",
        "Skeleton Length",
        "Bending energy",
    ]
    return np.asarray(res), res_colname, imo_selected


def write_in_html(
    base_folder_path,
    basefilename,
    valid_id,
    im_file,
    valid,
    basefilenamehead,
    t,
    area,
    p,
    h,
    blue_index,
    pix_mean,
    nendpoints,
    nbranches,
    skelength,
    bending,
):
    html = dedent(f"""\
    <b>ID: </b>{valid_id} - {im_file}<br>
    <b>Valid: </b>{valid}<br>
    <img src="{basefilenamehead}_ori.bmp"><br>
    <b>Area: </b>{area}<br>
    <b>Perimeter: </b>{p}<br>
    <img src="{basefilenamehead}_Skeleton.png"><br>
    <b>Texture (standard deviation of the gray level of the pixels): </b>{t}<br>
    <b>Entropy: </b>{h}<br>
    <b>Blue index: </b>{blue_index}<br>
    <b>Mean pixel value (grayscale): </b>{pix_mean}<br>
    <img src="{basefilenamehead}_Gray.png"><br>
    <b>NEndPoints: </b>{nendpoints}<br>
    <b>NBranches: </b>{nbranches}<br>
    <b>Skeleton Length </b>{skelength}<br>
    <b>Bending Energy: </b>{bending}<br>
    """)

    with open(path.join(base_folder_path, f"{basefilename}.html"), "w") as fd:
        fd.write(html)
