import cv2
import numpy as np
from lib.getbb import getbb
from lib.PCAxy import PCAxy
from lib.perim import perim
from lib.entropy import entropy


def gallus_sep_heads(imo, im_seg, im_file, print_image, manual_seg):
    n_ids, bw_im = cv2.connectedComponents(im_seg, connectivity=4)
    imo_selected = imo
    res = []

    valid_id = 1
    for ind_id in range(1, n_ids):

        basefilenamehead = f"{im_file}_h{valid_id}"
        basefilename = f"heads/{basefilenamehead}"

        imbb_seg, original_index, origin = getbb(bw_im, ind_id, 1, True)
        imbb = np.zeros((*imbb_seg.shape, 3), dtype=np.uint8)

        temp = imo[original_index]

        # head coordinates and matrix indexes
        im_x, im_y = np.where(imbb_seg > 0)
        im_index = (im_x, im_y)

        imbb[im_index] = temp

        # TODO: Chances extremamente altas dessas duas variáveis e chamada para PCAxy serem completamente inúteis nesse contexto (remover se for o caso)
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

        # converting to LAB
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
                cv2.imwrite(head_skeleton, SK_imbb_seg)

            # TODO: Validar se de fato devo salvar as imagens em bitmap (.bmp)
            # direto ou se devo seguir o formato selecionado da interface
            head_seg_fn = f"{basefilename}_seg.bmp"
            head_ori_fn = f"{basefilename}_ori.bmp"

            if print_image:
                cv2.imwrite(head_ori_fn, imbb)
                cv2.imwrite(head_seg_fn, imbb_seg.astype(np.uint8) * 255)

            # TODO: Validar o formato desse arquivo tbm (se deve ser png ou outro)
            head_gray_fn = f"{basefilename}_Gray.png"

            if print_image:
                cv2.imwrite(head_gray_fn, LAB_l.astype(np.uint8))

            # TODO: se der pau, pode ser porquê imo está em BGR, então o correto será:
            # imo_selected[original_index] = [0, 0, 255]
            # Consultar em https://chatgpt.com/g/g-p-693260cf8fd0819195b689d6eb55041e-tcc/c/6a3b4ca0-3e20-83e9-b854-359426198315
            imo_selected[original_index] = [255, 0, 0]

            # writing the results to an html file
            # TODO: adequar o caminho do arquivo html para o diretório base/auxiliary_files
            # (ou algo assim)
            # TODO: Extrair a escrita de arquivo html para uma função
            with open(f"{basefilename}.html", "w") as fd:
                fd.write(f"<b>ID: </b>{valid_id} - {im_file}<br>\n")
                fd.write(f"<b>Valid: </b>{valid}<br>\n")
                fd.write(f'<img src="{basefilenamehead}.bmp"><br>\n')
                fd.write(f"<b>Area: </b>{area}<br>\n")
                fd.write(f"<b>Perimeter: </b>{p}<br>\n")
                fd.write(f'<img src="{basefilenamehead}_Skeleton.png"><br>\n')
                fd.write(
                    "<b>Texture (standard deviation of the gray level of the pixels): </b>"
                    f"{t}<br>\n"
                )
                fd.write(f"<b>Entropy: </b>{h}<br>\n")
                fd.write(f"<b>Blue index: </b>{blue_index}<br>\n")
                fd.write(f"<b>Mean pixel value (grayscale): </b>{pix_mean}<br>\n")
                fd.write(f'<img src="{basefilenamehead}_Gray.png"><br>\n')
                fd.write(f"<b>NEndPoints: </b>{nendpoints}<br>\n")
                fd.write(f"<b>NBranches: </b>{nbranches}<br>\n")
                fd.write(f"<b>Skeleton Length </b>{skelength}<br>\n")
                fd.write(f"<b>Bending Energy: </b>{bending}<br>\n")

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
                f"{basefilename}.txt", np.asarray(resh).reshape(1, -1), fmt="%.10f"
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
