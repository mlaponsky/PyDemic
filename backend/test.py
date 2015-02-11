from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys

if __name__ == "__main__":
  app = QApplication(sys.argv)
  engine = QQmlApplicationEngine("Game.qml")
  engine.quit.connect(app.quit)
  sys.exit(app.exec_())
