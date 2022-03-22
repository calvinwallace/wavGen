from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from wav_generator import Exporter
import sys

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
        self.freq_label = QLabel('Frequenz (Hz):')
        self.factor_label = QLabel('Faktor:')
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

        # Hinzufügen-Button hinzufügen
        self.add_btn = QPushButton('Hinzufügen')
        self.layout.addWidget(self.add_btn)

        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.box_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

class Popup(QWidget):
    def __init__(self):
        super(Popup, self).__init__()
        self.setWindowTitle('Erfolg')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('WAV erfolgreich exportiert!')
        self.layout.addWidget(self.label)
        self.btn = QPushButton('OK')
        self.layout.addWidget(self.btn)
        self.adjustSize()

class MainWidget(QWidget):
    def __init__(self, add_win: AddWindow, popup: Popup):
        super(MainWidget, self).__init__()
        self.add_win = add_win
        self.popup = popup
        self.setWindowTitle('WAV-Generator')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.header_values = ['Name', 'Frequenz (Hz)', 'Faktor', 'Startzeitpunkt (s)', 'Endzeitpunkt (s)']
        self.create_layout()
        self.resize_tree()

    def create_layout(self):
        # QTreeWidget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.tree_widget.setHeaderLabels(self.header_values)
        self.layout.addWidget(self.tree_widget)

        # Button-Widget für Liste
        self.tree_btn_widget = QWidget()
        self.tree_btn_layout = QHBoxLayout()
        self.tree_btn_widget.setLayout(self.tree_btn_layout)
        self.layout.addWidget(self.tree_btn_widget)
        self.tree_btn_layout.setContentsMargins(0, 0, 0, 0)

        self.delete_btn = QPushButton('Löschen')
        self.tree_btn_layout.addWidget(self.delete_btn)
        self.delete_btn.setEnabled(False)

        self.add_btn = QPushButton('Hinzufügen')
        self.tree_btn_layout.addWidget(self.add_btn)

        # Button für Erstellen
        self.create_btn = QPushButton('Datei erstellen')
        self.layout.addWidget(self.create_btn)
        self.create_btn.setEnabled(False)

        self.adjustSize()
        self.setFixedWidth(500)

    def resize_tree(self):
        for i, _ in enumerate(self.header_values):
            self.tree_widget.resizeColumnToContents(i)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.add_win.close()
        self.popup.close()


class Controller:
    def __init__(self, add_window: AddWindow, popup: Popup):
        self.add_window = add_window
        self.popup = popup
        self.main_window = MainWidget(self.add_window, self.popup)
        self.exporter = Exporter(44100)

        self.init_signals()

    def run(self):
        self.main_window.show()

    def init_signals(self):
        self.main_window.add_btn.clicked.connect(self.handle_add)
        self.main_window.delete_btn.clicked.connect(self.handle_delete)
        self.main_window.create_btn.clicked.connect(self.handle_create)
        self.add_window.add_btn.clicked.connect(self.handle_new_signal)
        self.popup.btn.clicked.connect(self.popup.close)
        self.init_add_enter()

    def init_add_enter(self):
        self.add_window.name_box.returnPressed.connect(self.handle_new_signal)
        self.add_window.freq_box.returnPressed.connect(self.handle_new_signal)
        self.add_window.factor_box.returnPressed.connect(self.handle_new_signal)
        self.add_window.start_box.returnPressed.connect(self.handle_new_signal)
        self.add_window.end_box.returnPressed.connect(self.handle_new_signal)

    def handle_add(self):
        self.add_window.show()

    def handle_delete(self):
        root = self.main_window.tree_widget.invisibleRootItem()
        for item in self.main_window.tree_widget.selectedItems():
            name = item.text(0)
            for signal in self.exporter.signals:
                if signal.name == name:
                    self.exporter.signals.remove(signal)
            (item.parent() or root).removeChild(item)

        self.toggle_buttons()

    def handle_create(self):
        self.exporter.export_wav_file('gui_test.wav')
        self.popup.show()

    def handle_new_signal(self):
        name = self.add_window.name_box.text()
        freq = self.add_window.freq_box.text()
        factor = self.add_window.factor_box.text()
        start = self.add_window.start_box.text()
        end = self.add_window.end_box.text()

        self.add_window.name_box.setText('')
        self.add_window.freq_box.setText('')
        self.add_window.factor_box.setText('')
        self.add_window.start_box.setText('')
        self.add_window.end_box.setText('')

        self.exporter.create_new_signal(name, float(freq), float(factor), int(start), int(end))
        QTreeWidgetItem(self.main_window.tree_widget, [name, freq, factor, start, end])
        self.main_window.resize_tree()
        self.toggle_buttons()
        print(self.main_window.tree_widget.width())

    def toggle_buttons(self):
        if not self.exporter.is_empty:
            self.main_window.delete_btn.setEnabled(True)
            self.main_window.create_btn.setEnabled(True)
        else:
            self.main_window.delete_btn.setEnabled(False)
            self.main_window.create_btn.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_window = AddWindow()
    popup = Popup()
    controller = Controller(add_window, popup)
    controller.run()
    sys.exit(app.exec())
