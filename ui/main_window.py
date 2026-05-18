import os
import sys

if sys.platform.startswith("linux"):
    os.environ["LIBVA_DRIVER_NAME"] = "disable"

import webview
from pathlib import Path
from config.settings import WINDOW_TITLE, USER_HOME_DIR


class MainWindow:
    def __init__(self, controller):
        self.controller = controller

        self.controller.set_progress_callback(self.on_progress)
        self.controller.set_finished_callback(self.on_finished)

        # A partir dessa classe é possível expor métodos do controller python para o javascript.
        class API:
            def __init__(self, controller):
                self.controller = controller

            def select_folder(self):
                result = webview.windows[0].create_file_dialog(
                    dialog_type=webview.FileDialog.FOLDER,
                    directory=USER_HOME_DIR,
                    allow_multiple=True
                )
                if result:
                    folder = result[0]
                    return self.controller.add_selected_folder(folder)
                return None

            def remove_selected_folder(self, folder):
                return self.controller.remove_selected_folder(folder)

            def run_processing(self, processing_options: dict):
                self.controller.process_images(processing_options)
                return True

            def log(self, msg):
                print("[JS]", msg)

        self.api = API(controller)

    def run(self):
        html_path = Path(__file__).parent / "views" / "index.html"

        self.window = webview.create_window(
            WINDOW_TITLE,
            html_path.as_posix(),
            js_api=self.api
        )

        webview.start(gui="qt", http_server=True)

    def on_progress(self, index, total, filename):
        script = f"updateProgress({index}, {total}, '{filename}')"
        self.window.evaluate_js(script)

    def on_finished(self):
        self.window.evaluate_js("onFinished()")
