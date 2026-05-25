import logging
import threading
from datetime import datetime
from utils.file_utils import get_files_list_in_path, create_folder
from app.image_processor import load_image, cut_edges, write_image, rgb2gray, gallus_segseq
from config.settings import IMAGE_DEFAULT_FORMAT, SUPPORTED_IMAGE_FORMATS, DEFAULT_FOLDERS, USER_HOME_DIR, OUTPUT_FOLDER_BASE_NAME

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
            logger.warning(f"Couldn't remove folder {folder} from list because it not exists")

    def create_default_folders(self):
        OUTPUT_FOLDER_NAME = f"{OUTPUT_FOLDER_BASE_NAME}_{self.output_folder_sufix}"
        create_folder(USER_HOME_DIR, OUTPUT_FOLDER_NAME)
        for folder in DEFAULT_FOLDERS:
            create_folder(f"{USER_HOME_DIR}/{OUTPUT_FOLDER_NAME}", folder)
        self.output_folder_for_current_execution = f"{USER_HOME_DIR}/{OUTPUT_FOLDER_NAME}"

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
        
        self.output_folder_sufix = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        
        self.create_default_folders()

        self.processing_thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.processing_thread.start()
    
    def _worker(self):
        for current_folder in self.selected_folders:
            files = get_files_list_in_path(current_folder, self.selected_filetype)

            total = len(files)
            if total == 0:
                logger.info(f"No files with extension {self.selected_filetype} found inside the folder {current_folder}.")
                if(self.callback_finished):
                    self.callback_finished()
                return

            for index, file in enumerate(files, start=1):
                logger.info(f"valor de file: {file}")
                filename, file_extension = file.rsplit('.', maxsplit=1)
                full_path = f"{current_folder}/{file}"

                try:
                    image = load_image(full_path)
                    logger.info(f"Loaded {file}, shape={image.shape if image is not None else None}")
                    cut_edges_percentage = int(self.processing_options["cut_edges"])
                    if(cut_edges_percentage > 0):
                        image = cut_edges(image, cut_edges_percentage)

                    # converte imagem de RGB para Gray Scale
                    imageInGrayScale = rgb2gray(image)

                    # chama a função gallus_segseq passando a imagem em GrayScale e o nome do arquivo sem extenção
                    gallus_segseq(imageInGrayScale, filename)

                    # tira da memória a variável imageInGrayScale
                    # free(imageInGrayScale) // descobrir o análogo no python para evitar que o programa ocupe muita memória

                    # head separation routine
                    # se o arquivo segmentado existe em disco:
                    #   segmented_image = read(segmented_dir/filename_seg.extension)
                    #   
                    #   se a flag invert_im_seg estiver ativa:
                    #       segmented_image = invertImage(segmented_image)
                    #   
                    #   manual_seg = []   
                    #   
                    #   // Coletando métricas da imagem
                    #   res, res_colname, valid_seg_im = gallus_sep_heads(image, segmented_image, filename, true, manual_seg)
                    #   
                    #   writeImage(valid_seg_im, auxiliary_files/ + filename + "_seg2.png")
                    #   all_responses.append(res) # verificar/criar uma variável para armazenar todas as respostas do procesamento.
                    #   
                    #   for head_index in range(res.len()): #ou len(res)
                    #       cria string no formato 
                    #       "PASTA Arquivo nome_medida1_em_negrito medida1 nome_medida2_em_negrito medida2"
                    #       (métricas do espermatozoide segmentado)
                    #
                    #       // Cria strings com o caminho do html e imagem em formatp bmp da cabeça do espermatozoide
                    #       head_id_path = f"{current_folder}/heads/{im_file}_h{head_index}.bmp" 
                    #       head_id_html = f"{current_folder}/heads/{im_file}_h{head_index}.html"
                    #       all_image_file_str.append(head_id_path) # criar vetores para acumular esses valores
                    #   end_for
                    # end_if
                    #
                    # free(image)

                except FileNotFoundError:
                    logger.warning(f"File not found: {full_path}")
                
                if self.callback_progress:
                    self.callback_progress(index, total, file)
        
        if self.callback_finished:
            self.callback_finished()