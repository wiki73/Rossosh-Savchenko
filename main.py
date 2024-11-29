import sys
import random
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRect

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.pushButton.clicked.connect(self.draw_random_circle)

        self.circles = []

    def draw_random_circle(self):
        diameter = random.randint(20, 100)

        x = random.randint(0, self.width() - diameter)
        y = random.randint(0, self.height() - diameter)

        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.circles.append((x, y, diameter, color))

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        for x, y, diameter, color in self.circles:
            painter.setBrush(color)
            painter.drawEllipse(QRect(x, y, diameter, diameter))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
