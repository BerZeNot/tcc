import cv2
import numpy as np
import os.path as path

from lib.getbb import getbb
from lib.PCAxy import PCAxy
from lib.perim import perim
from lib.entropy import entropy

from lib.draw_pca_vectors import DrawPCAVectors
from lib.get_extremities import GetExtremities
from lib.mirror_im import MirrorIm
from lib.Symmetry import Symmetry

from textwrap import dedent


def bull_sep_heads(
    imo,
    im_seg,
    im_file,
    print_image,
    base_folder_path,
):
    """
    Python version of bull_sep_heads.m

    The manual segmentation is currently ignored, as in the current version
    of the project there is no support for manual validation.
    """

    # Connected components (background == 0)
    n_ids, bw_im = cv2.connectedComponents(
        im_seg.astype(np.uint8),
        connectivity=4,
    )

    res = []

    pad = int(np.ceil(imo.shape[0] / 5))

    imopad = np.pad(
        imo,
        ((pad, pad), (pad, pad), (0, 0)),
        mode="constant",
    )

    valid_seg_im = im_seg.copy()

    #
    # Manual segmentation intentionally ignored
    # because this inicial version won't
    # support it.
    #
    valid_id = 0

    for ind_id in range(1, n_ids):

        basefilenamehead = f"{im_file}_h{valid_id}"

        basefilename = path.join(
            "heads",
            basefilenamehead,
        )

        basefilename_valid = path.join(
            "valid_heads",
            basefilenamehead,
        )

        #
        # Load precomputed measurements if available
        #
        txt_file = path.join(
            base_folder_path,
            f"{basefilename}.txt",
        )

        if path.exists(txt_file):

            measurements = np.loadtxt(txt_file)

            valid_head = measurements[1]
            area = measurements[2]
            p = measurements[3]
            elongation = measurements[4]
            sym_index = measurements[5]
            t = measurements[6]
            h = measurements[7]
            pca_len = measurements[8]
            pca_wdt = measurements[9]
            blue_index = measurements[10]
            pix_mean = measurements[11]

        #
        # Bounding box
        #
        imbb_seg, original_index, origin = getbb(
            bw_im,
            ind_id,
            1,
            True,
        )

        imbb = np.zeros(
            (*imbb_seg.shape, 3),
            dtype=np.uint8,
        )

        #
        # Copy RGB pixels from original image
        #
        temp = imo[original_index]

        #
        # Object coordinates
        #
        im_x, im_y = np.where(imbb_seg > 0)

        im_index = (im_x, im_y)

        imbb[im_index] = temp

        valid_head = -1

        # Center of mass
        im_xm = np.mean(im_x)
        im_ym = np.mean(im_y)
        cmass = np.asarray([im_xm, im_ym])

        #
        # Area
        #
        area = im_x.size

        #
        # Perimeter
        #
        p = perim(imbb_seg)

        #
        # Principal Component Analysis
        #
        PCAFilename = f"{basefilename}_PCA.png"

        aVal, aVec = PCAxy(
            im_x,
            im_y,
        )

        imPCA = DrawPCAVectors(
            imbb_seg.astype(np.float32),
            cmass,
            aVec,
        )

        if print_image:
            cv2.imwrite(
                path.join(
                    base_folder_path,
                    PCAFilename,
                ),
                (imPCA * 255).astype(np.uint8),
            )

        #
        # PCA Length
        #
        pca_len = GetExtremities(
            imbb_seg,
            cmass,
            aVec[:, 0],
        )

        #
        # PCA Width
        #
        pca_wdt = GetExtremities(
            imbb_seg,
            cmass,
            aVec[:, 1],
        )

        #
        # Elongation
        #
        if aVal[1] != 0:
            elongation = aVal[0] / aVal[1]
        else:
            elongation = 0

        #
        # Mirror image
        #
        mirrorFilename = f"{basefilename}_Mirror.png"

        imMirror = MirrorIm(
            imbb_seg,
            cmass,
            aVec[:, 0],
        )

        if print_image:
            cv2.imwrite(
                path.join(
                    base_folder_path,
                    mirrorFilename,
                ),
                (imMirror * 255).astype(np.uint8),
            )

        #
        # Symmetry
        #
        symmetryFilename = f"{basefilename}_Symmetry.png"

        sym_index, joint_im = Symmetry(
            imbb_seg,
            imMirror,
        )

        if print_image:
            max_value = np.max(joint_im)

            if max_value > 0:
                img = (joint_im / max_value * 255).astype(np.uint8)
            else:
                img = joint_im.astype(np.uint8)

            cv2.imwrite(
                path.join(
                    base_folder_path,
                    symmetryFilename,
                ),
                img,
            )

        #
        # Save segmented head
        #
        head_seg_fn = f"{basefilename}_seg.bmp"
        head_ori_fn = f"{basefilename}.bmp"

        if print_image:
            cv2.imwrite(
                path.join(
                    base_folder_path,
                    head_ori_fn,
                ),
                imbb,
            )

            cv2.imwrite(
                path.join(
                    base_folder_path,
                    head_seg_fn,
                ),
                imbb_seg.astype(np.uint8) * 255,
            )

        lab = cv2.cvtColor(
            imbb,
            cv2.COLOR_RGB2LAB,
        )

        LAB_l = lab[:, :, 0].astype(np.float64)
        LAB_a = lab[:, :, 1].astype(np.float64) - 128
        LAB_b = lab[:, :, 2].astype(np.float64) - 128

        head_gray_fn = f"{basefilename}_Gray.png"

        #
        # Mean gray value
        #
        pix_mean = np.mean(LAB_l[im_index])

        if print_image:
            cv2.imwrite(
                path.join(
                    base_folder_path,
                    head_gray_fn,
                ),
                LAB_l.astype(np.uint8),
            )

        #
        # Texture
        #
        t = np.std(LAB_l[im_index])

        #
        # Entropy
        #
        h = entropy(
            LAB_l[im_index],
            255,
        )

        #
        # Blue Index
        #

        mask_path = path.join(
            base_folder_path,
            "..",
            "lab_all_mask.png",
        )

        if path.exists(mask_path):

            mask_lab = cv2.imread(
                mask_path,
                cv2.IMREAD_GRAYSCALE,
            )

            LAB_a_h = np.round(LAB_a[im_index] + 111).astype(int)

            LAB_b_h = np.round(LAB_b[im_index] + 111).astype(int)

            #
            # Same indexing used by the Octave code
            #

            linear_index = (LAB_a_h - 1) * 221 + LAB_b_h

            linear_index = np.clip(
                linear_index,
                0,
                mask_lab.size - 1,
            )

            blue_index = np.sum(mask_lab.ravel()[linear_index]) / len(linear_index)

        else:
            blue_index = 0

        #
        # Automatic validation
        #

        if elongation <= 6 and sym_index > 0.8:
            valid_head = 1

        #
        # Remove invalid heads
        #

        if valid_head == -1:
            valid_seg_im[original_index] = 0

        else:

            if print_image:

                valid_head_seg_fn = f"{basefilename_valid}_seg.bmp"

                valid_head_ori_clip_fn = f"{basefilename_valid}.bmp"

                valid_head_ori_fn = f"{basefilename_valid}_context.bmp"

                #
                # Context image
                #

                sx, sy = imbb_seg.shape

                origin_pad = (
                    origin[0] + pad,
                    origin[1] + pad,
                )

                imbb_or = imopad[
                    origin_pad[0] : origin_pad[0] + sx,
                    origin_pad[1] : origin_pad[1] + sy,
                ]

                cv2.imwrite(
                    path.join(
                        base_folder_path,
                        valid_head_ori_clip_fn,
                    ),
                    imbb,
                )

                cv2.imwrite(
                    path.join(
                        base_folder_path,
                        valid_head_ori_fn,
                    ),
                    imbb_or,
                )

                cv2.imwrite(
                    path.join(
                        base_folder_path,
                        valid_head_seg_fn,
                    ),
                    imbb_seg.astype(np.uint8) * 255,
                )
        write_in_html(
            base_folder_path=base_folder_path,
            basefilename=basefilename,
            head_filename=basefilenamehead,
            image_filename=im_file,
            head_id=valid_id,
            valid_head=valid_head,
            area=area,
            perimeter=p,
            elongation=elongation,
            symmetry=sym_index,
            texture=t,
            entropy_value=h,
            pca_length=pca_len,
            pca_width=pca_wdt,
            blue_index=blue_index,
            pix_mean=pix_mean,
        )

        #
        # Save measurements
        #
        resh = [
            valid_id,
            valid_head,
            area,
            p,
            elongation,
            sym_index,
            t,
            h,
            pca_len,
            pca_wdt,
            blue_index,
            pix_mean,
        ]

        res.append(resh)

        np.savetxt(
            path.join(
                base_folder_path,
                f"{basefilename}.txt",
            ),
            np.asarray(resh).reshape(1, -1),
            fmt="%.10f",
        )

        valid_id += 1

    #
    # Column names
    #
    res_colname = [
        "id",
        "Valid_head",
        "Area",
        "Perimeter",
        "Elongation",
        "Symmetry",
        "Texture",
        "Entropy",
        "PCA length",
        "PCA width",
        "Blue index",
        "Mean pixel value (grayscale)",
    ]

    return (
        np.asarray(res),
        res_colname,
        valid_seg_im,
    )


from textwrap import dedent


def write_in_html(
    base_folder_path,
    basefilename,
    head_filename,
    image_filename,
    head_id,
    valid_head,
    area,
    perimeter,
    elongation,
    symmetry,
    texture,
    entropy_value,
    pca_length,
    pca_width,
    blue_index,
    pix_mean,
):

    html = dedent(f"""\
        <b>ID:</b> {head_id} - {image_filename}<br>

        <img src="{head_filename}.bmp"><br>

        <b>Valid:</b> {valid_head}<br>

        <b>Area:</b> {area}<br>

        <b>Perimeter:</b> {perimeter}<br>

        <b>Elongation:</b> {elongation}<br>

        <b>Symmetry:</b> {symmetry}<br>

        <img src="{head_filename}_Symmetry.png"><br>

        <b>Texture:</b> {texture}<br>

        <b>Entropy:</b> {entropy_value}<br>

        <b>PCA length:</b> {pca_length}<br>

        <b>PCA width:</b> {pca_width}<br>

        <img src="{head_filename}_PCA.png"><br>

        <b>Blue index:</b> {blue_index}<br>

        <b>Mean pixel value (grayscale):</b> {pix_mean}<br>

        <img src="{head_filename}_Gray.png"><br>
        """)

    with open(
        path.join(
            base_folder_path,
            f"{basefilename}.html",
        ),
        "w",
    ) as fd:
        fd.write(html)
