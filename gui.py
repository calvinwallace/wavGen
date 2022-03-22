from PyQt6.QtWidgets import *
from wav_generator import Exporter
import sys


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.setWindowTitle('WAV-Generator')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.header_values = ['Name', 'Frequenz', 'Faktor', 'Start', 'Ende']
        self.create_layout()

    def create_layout(self):
        # QTreeWidget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(self.header_values)
        for i, _ in enumerate(self.header_values):
            self.tree_widget.resizeColumnToContents(i)
        self.layout.addWidget(self.tree_widget)

        # Button-Widget für Liste
        self.tree_btn_widget = QWidget()
        self.tree_btn_layout = QHBoxLayout()
        self.tree_btn_widget.setLayout(self.tree_btn_layout)
        self.layout.addWidget(self.tree_btn_widget)
        self.tree_btn_layout.setContentsMargins(0, 0, 0, 0)

        self.delete_btn = QPushButton('Löschen')
        self.tree_btn_layout.addWidget(self.delete_btn)

        self.add_btn = QPushButton('Hinzufügen')
        self.tree_btn_layout.addWidget(self.add_btn)

        # Button für Erstellen
        self.create_btn = QPushButton('Datei erstellen')
        self.layout.addWidget(self.create_btn)

        self.adjustSize()


class AddWindow(QWidget):
    def __init__(self):
        super(AddWindow, self).__init__()
        self.setWindowTitle('Frequenz hinzufügen')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.create_layout()

    def create_layout(self):
        # Widget für Content
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.layout.addWidget(self.content_widget)

        # Widget für Text
        self.text_widget = QWidget()
        self.text_layout = QVBoxLayout()
        self.text_widget.setLayout(self.text_layout)
        self.content_layout.addWidget(self.text_widget)

        # Widget für Textboxen
        self.box_widget = QWidget()
        self.box_layout = QVBoxLayout()
        self.box_widget.setLayout(self.box_layout)
        self.content_layout.addWidget(self.box_widget)

        # Labels hinzufügen
        self.name_label = QLabel('Name:')
        self.freq_label = QLabel('Frequenz:')
        self.factor_label = QLabel('Faktor (Hz):')
        self.start_label = QLabel('Startzeitpunkt (s):')
        self.end_label = QLabel('Endzeitpunkt (s):')

        self.text_layout.addWidget(self.name_label)
        self.text_layout.addWidget(self.freq_label)
        self.text_layout.addWidget(self.factor_label)
        self.text_layout.addWidget(self.start_label)
        self.text_layout.addWidget(self.end_label)

        # Textboxen hinzufügen
        self.name_box = QLineEdit()
        self.freq_box = QLineEdit()
        self.factor_box = QLineEdit()
        self.start_box = QLineEdit()
        self.end_box = QLineEdit()

        self.box_layout.addWidget(self.name_box)
        self.box_layout.addWidget(self.freq_box)
        self.box_layout.addWidget(self.factor_box)
        self.box_layout.addWidget(self.start_box)
        self.box_layout.addWidget(self.end_box)

        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.box_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)



class Controller:
    def __init__(self, main_window: MainWidget, add_window: AddWindow):
        self.main_window = main_window
        self.add_window = add_window

        self.init_signals()

    def run(self):
        self.main_window.show()

    def init_signals(self):
        self.main_window.add_btn.clicked.connect(self.handle_add)
        self.main_window.delete_btn.clicked.connect(self.handle_delete)
        self.main_window.create_btn.clicked.connect(self.handle_create)

    def handle_add(self):
        self.add_window.show()

    def handle_delete(self):
        pass

    def handle_create(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller(MainWidget(), AddWindow())
    controller.run()
    sys.exit(app.exec())
