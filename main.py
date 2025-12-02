from ui.main_window import MainWindow
from app.controller import AppController

if __name__ == "__main__":
    controller = AppController()
    app = MainWindow(controller)
    app.run()