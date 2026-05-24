import logging
from ui.main_window import MainWindow
from app.controller import AppController

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    controller = AppController()
    app = MainWindow(controller)
    app.run()