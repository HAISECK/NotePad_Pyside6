import sys
import getpass
import time
import os
from PySide6 import QtCore, QtWidgets, QtGui

number_windows = 1

class Notebook(QtWidgets.QMainWindow):
    all_windows = []
    def __init__(self):
        super().__init__()  
        self.start_name = 'Безымянный'
        self.setWindowTitle(self.start_name)
        self.text_arena = QtWidgets.QTextEdit()
        self.setCentralWidget(self.text_arena)
        menu_bar = self.menuBar()
        bar_file = menu_bar.addMenu("Файл")
        bar_editing = menu_bar.addMenu("Правка")
        bar_view = menu_bar.addMenu("Вид")

        # бар фаил
        new_window_actions = QtGui.QAction("Новое окно", self)
        open_actions = QtGui.QAction('Открыть   Ctrl+O', self)
        save_actions = QtGui.QAction('Сохранить   Ctrl+S', self)
        exit_actions = QtGui.QAction('Выход', self)

        bar_file.addAction(new_window_actions)
        bar_file.addAction(open_actions)
        bar_file.addAction(save_actions)
        bar_file.addSeparator()
        bar_file.addAction(exit_actions)

        new_window_actions.triggered.connect(self.on_new_window)
        open_actions.triggered.connect(self.on_open)
        save_actions.triggered.connect(self.on_save)
        exit_actions.triggered.connect(self.close)

        # бар правок
        cancellation_actions = QtGui.QAction('Отмена   Ctrl+Z', self)
        cut_actions = QtGui.QAction('Вырезать', self)
        copy_actions= QtGui.QAction('Копировать', self)
        insert_actions = QtGui.QAction('Вставить', self)
        delete_actions = QtGui.QAction('Удалить', self)
        find_actions = QtGui.QAction('Найти   Ctrl+F', self)
        replace_actions = QtGui.QAction('Заменить', self)
        go_actions = QtGui.QAction('Перейти   Ctrl+G', self)
        select_all_actions = QtGui.QAction('Выделить всё', self)
        time_and_date_actions = QtGui.QAction('Время и дата', self)

        bar_editing.addAction(cancellation_actions)
        bar_editing.addAction(cut_actions)
        bar_editing.addAction(copy_actions)
        bar_editing.addAction(insert_actions)
        bar_editing.addAction(delete_actions)
        bar_editing.addSeparator()
        bar_editing.addAction(find_actions)
        bar_editing.addAction(replace_actions)
        bar_editing.addAction(go_actions)
        bar_editing.addSeparator()
        bar_editing.addAction(select_all_actions)
        bar_editing.addAction(time_and_date_actions)

        cancellation_actions.triggered.connect(self.on_cancellation)
        cut_actions.triggered.connect(self.on_cut)
        copy_actions.triggered.connect(self.on_copy)
        insert_actions.triggered.connect(self.on_insert)
        delete_actions.triggered.connect(self.on_delete)
        find_actions.triggered.connect(self.on_find)
        replace_actions.triggered.connect(self.on_replace)
        go_actions.triggered.connect(self.on_go)
        select_all_actions.triggered.connect(self.on_select_all)
        time_and_date_actions.triggered.connect(self.on_time_and_date)

        cut_actions.setEnabled(False)
        copy_actions.setEnabled(False)
        delete_actions.setEnabled(False)

        save_actions.setShortcut("Ctrl+S")
        open_actions.setShortcut("Ctrl+O")
        find_actions.setShortcut("Ctrl+F")
        go_actions.setShortcut("Ctrl+G")
        cancellation_actions.setShortcut("Ctrl+Z")

        self.text_arena.copyAvailable.connect(cut_actions.setEnabled)
        self.text_arena.copyAvailable.connect(copy_actions.setEnabled)
        self.text_arena.copyAvailable.connect(delete_actions.setEnabled)

    @QtCore.Slot()
    def on_new_window(self):
        global number_windows
        new_window = Notebook()
        new_window.resize(600 - (number_windows*20), 400 - (number_windows*20))
        number_windows+=1
        self.all_windows.append(new_window)
        new_window.show()

    @QtCore.Slot()
    def on_open(self):
        user_name = getpass.getuser()
        file_path, file_format = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', f"C:/Users/{user_name}/Documents", "Текстовые файлы (*.txt)")
        if file_path == '':
            return
        else:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_arena.setPlainText(file.read())
                self.start_name = os.path.basename(file_path)
                self.setWindowTitle(self.start_name)

    @QtCore.Slot()
    def on_save(self):
        user_name = getpass.getuser()
        file_path, file_format = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранение', f"C:/Users/{user_name}/Documents", "Текстовые файлы (*.txt)")
        if file_path == '':
            return
        else:
            text_plain = str(self.text_arena.toPlainText())
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_plain)
                self.start_name = os.path.basename(file_path)
                self.setWindowTitle(self.start_name)

    @QtCore.Slot()
    def on_cancellation(self):
        self.text_arena.undo()

    @QtCore.Slot()
    def on_cut(self):
        self.text_arena.cut()

    @QtCore.Slot()
    def on_copy(self):
        self.text_arena.copy()

    @QtCore.Slot()
    def on_insert(self):
        self.text_arena.paste()

    @QtCore.Slot()
    def on_delete(self):
        self.text_arena.textCursor().removeSelectedText()

    @QtCore.Slot()
    def on_find(self):
        text_find, yes_or_no = QtWidgets.QInputDialog.getText(self, "Найти", "Что ищем:")
        if yes_or_no:
            self.text_arena.find(text_find)

    @QtCore.Slot()
    def on_replace(self):
        first_word, yes_and_no = QtWidgets.QInputDialog.getText(self, "Заменить", "Что заменить:")
        if yes_and_no:
            second_word, yes_or_no = QtWidgets.QInputDialog.getText(self, "Заменить", "На что заменить:")
            if yes_or_no:
                text = self.text_arena.toPlainText()
                new_text = text.replace(first_word, second_word)
                self.text_arena.setPlainText(new_text)

    @QtCore.Slot()
    def on_go(self):
        total_lines = self.text_arena.document().blockCount()
        line_number, yes_or_no = QtWidgets.QInputDialog.getInt(self, "Перейти к странице", f"Введите номер страницы (1 - {total_lines}):")
        if yes_or_no:
            if line_number <= total_lines:
                cursor = self.text_arena.textCursor()
                cursor.setPosition(self.text_arena.document().findBlockByNumber(line_number - 1).position())
                self.text_arena.setTextCursor(cursor)

    @QtCore.Slot()
    def on_select_all(self):
        self.text_arena.selectAll()

    @QtCore.Slot()
    def on_time_and_date(self):
        current_time = time.strftime("%H:%M %d.%m.%Y")
        self.text_arena.insertPlainText(current_time)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Notebook()
    widget.resize(600, 400)
    widget.show()

    sys.exit(app.exec())