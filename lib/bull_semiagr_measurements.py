import numpy as np


def bull_semiagr_measurements(all_res: np.ndarray):

    id_pm = 10

    number_heads_reference = min(6, all_res.shape[0])

    all_pix_mean = all_res[:, id_pm]

    all_pix_mean_sort = np.sort(all_pix_mean)[::-1]

    ref_pix_mean = np.mean(all_pix_mean_sort[:number_heads_reference])

    dev_pix_mean = 100 * np.abs(all_res[:, id_pm] - ref_pix_mean) / 255.0

    dev_pix_mean_class = (dev_pix_mean < 5).astype(np.uint8)

    res = np.column_stack((dev_pix_mean, dev_pix_mean_class))

    res_colname = [
        "Porc. desvio valor medio",
        "Class Bom(1) Ruim(0)",
    ]

    return res, res_colname
