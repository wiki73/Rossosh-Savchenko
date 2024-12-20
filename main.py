import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QLabel


class AddEditCoffeeForm(QDialog):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('coffee.sqlite')
        self.cursor = self.conn.cursor()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add_coffe)
        self.leble = QLabel()

    def check_line_edit(self):
        print(any([self.nameLabel.text() != '', self.roastLabel.text() != '', self.groundLabel.text() != '',
                   self.flavorLabel.text() != '', self.priceLabel.text() != '', self.volumeLabel.text() != '']))
        return self.nameLabel.text()

    def add_coffe(self):
        if not self.check_line_edit():
            self.status_lable.setText('Поля не заполнены')
        else:
            name = self.nameLabel.text()
            roast_degree = self.roastLabel.text()
            grind_type = self.groundLabel.text()
            taste_description = self.flavorLabel.text()
            price = self.priceLabel.text()
            package_volume = self.volumeLabel.text()
            self.cursor.execute(
                "INSERT INTO coffee (name, roast_level, ground, flavor_description,"
                " price, package_volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast_degree, grind_type, taste_description, price, package_volume)
            )

            self.conn.commit()  # Сохраняем изменения
            QMessageBox.information(self, "Success", "Coffee record saved successfully!")


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.loadButton.clicked.connect(self.load_coffee_data)
        self.coffee_list.currentItemChanged.connect(self.display_coffee_details)

        self.conn = sqlite3.connect('coffee.sqlite')
        self.cursor = self.conn.cursor()
        self.addButton.clicked.connect(self.run)

    def run(self):
        self.windoww = AddEditCoffeeForm()
        self.windoww.show()

    def load_coffee_data(self):
        try:
            self.cursor.execute("SELECT id, name FROM coffee")
            coffee_data = self.cursor.fetchall()
            self.coffee_list.clear()
            for coffee in coffee_data:
                self.coffee_list.addItem(f"{coffee[0]}: {coffee[1]}")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def display_coffee_details(self, current):
        if current is None:
            return

        coffee_id = current.text().split(":")[0]  # Получаем ID кофе из текста
        try:
            self.cursor.execute("SELECT * FROM coffee WHERE id = ?", (coffee_id,))
            coffee = self.cursor.fetchone()

            if coffee:
                self.nameLabel.setText(coffee[1])
                self.roastLabel.setText(coffee[2])
                self.groundLabel.setText("Молотый" if coffee[3] else "В зернах")
                self.flavorLabel.setText(coffee[4])
                self.priceLabel.setText(f"{coffee[5]} руб.")
                self.volumeLabel.setText(f"{coffee[6]} г.")
            else:
                QMessageBox.warning(self, "Внимание", "Кофе не найден.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
