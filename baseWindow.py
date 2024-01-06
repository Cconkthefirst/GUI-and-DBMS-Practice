from PyQt6.QtWidgets import QMainWindow  # Import the QMainWindow class from PyQt6

#====================================================================================
# SOURCES:
# https://doc.qt.io/qtforpython-6/
# https://dev.mysql.com/doc/
# https://realpython.com/qt-designer-python/
# https://www.w3schools.com/sql/
# https://www.geeksforgeeks.org/creating-tables-with-prettytable-library-python/
# https://pypi.org/project/prettytable/
# https://www.w3schools.com/python/python_lambda.asp
# https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
# https://www.pythonguis.com/tutorials/pyqt6-layouts/
# https://regex101.com/
# https://www.geeksforgeeks.org/string-formatting-in-python/
# https://www.w3schools.com/python/python_dictionaries.asp
# https://www.geeksforgeeks.org/python-dictionary/
# https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
# https://www.pythonguis.com/tutorials/pyqt6-dialogs/
# https://www.youtube.com/watch?v=Cc_zaUbF4LM
# https://www.youtube.com/watch?v=N2JfygnWJaA
#====================================================================================

class tempWindow(QMainWindow):
    def __init__(self, title, stylesheet):      # Constructor for the 'tempWindow' class
        super().__init__()                      # Call the constructor of the parent class
        self.setWindowTitle(title)              # Set the window title
        self.setGeometry(100, 100, 800, 600)    # Set the window's position and size
        self.setStyleSheet(stylesheet)          # Set the stylesheet for the window