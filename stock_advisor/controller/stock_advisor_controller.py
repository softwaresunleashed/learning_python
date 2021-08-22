from view.stock_advisor_base_window import *
import sys


app = QApplication(sys.argv)
window = Ui_MainWindow()
window.setupUi()
window.show()

sys.exit(app.exec_())

