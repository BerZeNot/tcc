import os.path as path
import logging
import threading
import numpy as np
from datetime import datetime
from textwrap import dedent
from utils.file_utils import get_files_list_in_path, create_folder
from lib.gallus_sep_heads import gallus_sep_heads
from lib.bull_sep_heads import bull_sep_heads
from lib.bull_semiagr_measurements import bull_semiagr_measurements
from app.image_processor import (
    load_image,
    cut_edges,
    write_image,
    rgb2gray,
    gallus_segseq,
    bull_segseq,
    invert_image,
)
from config.settings import (
    IMAGE_DEFAULT_FORMAT,
    SUPPORTED_IMAGE_FORMATS,
    DEFAULT_FOLDERS,
    USER_HOME_DIR,
    OUTPUT_FOLDER_BASE_NAME,
)

logger = logging.getLogger(__name__)


class AppController:
    def __init__(self):
        self.selected_folders = None
        self.selected_filetype = IMAGE_DEFAULT_FORMAT
        self.filetype_options = SUPPORTED_IMAGE_FORMATS
        self.processing_thread = None
        self.callback_progress = None
        self.callback_finished = None
        self.output_folder_sufix = None
        self.output_folder_for_current_execution = None
        self.processing_options = None

    def add_selected_folder(self, folder: str):
        if not self.selected_folders:
            self.selected_folders = list()

        if folder in self.selected_folders:
            return None

        self.selected_folders.append(folder)
        return folder

    def remove_selected_folder(self, folder: str):
        if not self.selected_folders:
            return
        try:
            self.selected_folders.remove(folder)
        except ValueError:
            logger.warning(
                f"Couldn't remove folder {folder} from list because it not exists"
            )

    def create_default_folders(self):
        OUTPUT_FOLDER_NAME = f"{OUTPUT_FOLDER_BASE_NAME}_{self.output_folder_sufix}"
        create_folder(USER_HOME_DIR, OUTPUT_FOLDER_NAME)
        for folder in DEFAULT_FOLDERS:
            create_folder(f"{USER_HOME_DIR}/{OUTPUT_FOLDER_NAME}", folder)
        self.output_folder_for_current_execution = (
            f"{USER_HOME_DIR}/{OUTPUT_FOLDER_NAME}"
        )

    def set_progress_callback(self, callback):
        self.callback_progress = callback

    def set_finished_callback(self, callback):
        self.callback_finished = callback

    def process_images(self, processing_options: dict):
        if processing_options:
            self.processing_options = processing_options

        if not self.selected_folders:
            logger.warning("No folders selected!")
            return

        if self.processing_thread and self.processing_thread.is_alive():
            logger.warning("Processing already running")
            return

        self.output_folder_sufix = datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss")

        self.create_default_folders()

        self.processing_thread = threading.Thread(target=self._worker, daemon=True)
        self.processing_thread.start()

    def _worker(self):
        all_str = []
        all_str_with_precision = []
        all_results = []
        all_html_file_str = []
        all_image_file_str = []

        selected_sperma_type = self.processing_options["sperm_type"]
        logger.info(f"SELECTED SPERMA TYPE: {selected_sperma_type}")

        for current_folder in self.selected_folders:
            files = get_files_list_in_path(current_folder, self.selected_filetype)

            total = len(files)
            if total == 0:
                logger.info(
                    f"No files with extension {self.selected_filetype} found inside the folder {current_folder}."
                )
                if self.callback_finished:
                    self.callback_finished()
                return

            for index, file in enumerate(files, start=1):
                logger.info(f"valor de file: {file}")
                filename = file.rsplit(".", maxsplit=1)[0]
                full_path = path.join(current_folder, file)

                try:
                    aux_files_path = path.join(
                        self.output_folder_for_current_execution, "auxiliary_files"
                    )
                    image = load_image(full_path)
                    logger.info(
                        f"Loaded {file}, shape={image.shape if image is not None else None}"
                    )
                    cut_edges_percentage = int(self.processing_options["cut_edges"])
                    if cut_edges_percentage > 0:
                        image = cut_edges(image, cut_edges_percentage)

                    seg_file_name = f"{filename}_seg.png"

                    segmented_image_path = path.join(aux_files_path, seg_file_name)

                    if (
                        not path.exists(segmented_image_path)
                        or self.processing_options["segment_images"]
                    ):
                        imageInGrayScale = rgb2gray(image)

                        if selected_sperma_type == "GALLUS":
                            gallus_segseq(imageInGrayScale, filename, aux_files_path)

                        if selected_sperma_type == "BULL":
                            bull_segseq(imageInGrayScale, filename, aux_files_path)

                        del imageInGrayScale

                    # head separation routine
                    if path.exists(segmented_image_path):
                        segmented_image = load_image(
                            segmented_image_path, convert2grayscale=True
                        )

                        if self.processing_options["invert_segmented_images"]:
                            segmented_image = invert_image(segmented_image)

                        if selected_sperma_type == "GALLUS":
                            res, res_colname, valid_seg_im = gallus_sep_heads(
                                image,
                                segmented_image,
                                filename,
                                True,
                                self.output_folder_for_current_execution,
                            )

                        if selected_sperma_type == "BULL":
                            res, res_colname, valid_seg_im = bull_sep_heads(
                                image,
                                segmented_image,
                                filename,
                                True,
                                self.output_folder_for_current_execution,
                            )

                        write_image(
                            path.join(aux_files_path, f"{filename}_seg2.png"),
                            valid_seg_im,
                        )

                        all_results.append(res)

                        for head_index in range(res.shape[0]):

                            # cria string no formato
                            # "PASTA Arquivo nome_medida1_em_negrito medida1 nome_medida2_em_negrito medida2"
                            tmp_head_str = f"{current_folder} {filename} "
                            for column_index in range(res.shape[1]):
                                tmp_head_str += f"<b>{res_colname[column_index]}</b>: {res[head_index][column_index]:.2f}"
                            all_str.append(tmp_head_str)
                            # Cria strings com o caminho do html e imagem em formatp bmp da cabeça do espermatozoide

                            head_id_path = path.join(
                                current_folder,
                                "heads",
                                f"{seg_file_name}_h{head_index}.bmp",
                            )
                            head_id_html = path.join(
                                self.output_folder_for_current_execution,
                                "heads",
                                f"{filename}_h{head_index}.html",
                            )

                            all_image_file_str.append(head_id_path)
                            all_html_file_str.append(head_id_html)

                            values_with_precision = " ".join(
                                f"{v:.18e}" for v in res[head_index]
                            )
                            str_with_precision = f"{head_id_path} {head_id_html} {current_folder} {filename} {values_with_precision}"
                            all_str_with_precision.append(str_with_precision)

                    del image

                except FileNotFoundError as e:
                    logger.warning(e)

                if self.callback_progress:
                    self.callback_progress(index, total, file)

        all_results_matrix = np.vstack(all_results)
        all_res_sa, all_res_sa_colname = bull_semiagr_measurements(all_results_matrix)

        res_colname.extend(all_res_sa_colname)
        all_results_matrix = np.hstack((all_results_matrix, all_res_sa))

        results_file_path = path.join(
            self.output_folder_for_current_execution, "results.txt"
        )
        with open(results_file_path, "w") as fd:
            for line in all_str_with_precision:
                fd.write(line + "\n")

        k = np.argsort(-all_results_matrix, axis=0)

        mtype_file_path = path.join(
            self.output_folder_for_current_execution, "mtype.html"
        )

        with open(mtype_file_path, "w") as fmtype:
            fmtype.write("<html><body>")

            for column_index, column_name in enumerate(res_colname):

                html_path = path.join(
                    self.output_folder_for_current_execution,
                    f"result_sort_{column_name}.html",
                )

                with open(html_path, "w") as fh:
                    fh.write(dedent(f"""<html>
                        <head>
                        <title>Sort by {column_name}</title>
                        </head>
                        <body>
                        """))

                    for row_index in k[:, column_index]:
                        fh.write(
                            f'<a target="bullsperm" '
                            f'href="{all_html_file_str[row_index]}">'
                            f"{column_name}: "
                            f"{all_results_matrix[row_index, column_index]}"
                            f"</a><br>\n"
                        )
                    fh.write("</body></html>")
                fmtype.write(
                    f'<a target="measurements" '
                    f'href="result_sort_{column_name}.html">'
                    f"{column_name}</a> / "
                )
            fmtype.write("</body></html>")

        if self.callback_finished:
            self.callback_finished()
