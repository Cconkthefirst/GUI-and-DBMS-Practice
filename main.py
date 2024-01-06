import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from loginWindow import loginWindow
from interactionWindow import interactionWindow

#====================================================================================
# SOURCES:
# Petes gitHub tutorial (I lost the link to them)
# Class Book
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

#====================================================================================
class mainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create login window
        self.loginWindow = loginWindow()
        self.loginWindow.show()

        self.loginWindow.passwordInput.returnPressed.connect(self.handleLoginSubmit)
        self.loginWindow.usernameInput.returnPressed.connect(self.handleLoginSubmit)
        # Connect the submit button click to the function that handles the transition
        self.loginWindow.submitButton.clicked.connect(self.handleLoginSubmit)

    def handleLoginSubmit(self):
        # Assuming you have a function to validate login information
        # For example, check username and password against a database
        validLogin = self.validateLogin(
            self.loginWindow.usernameInput.text(), self.loginWindow.passwordInput.text()
        )

        if validLogin:
            self.loginWindow.errorMessage.setText("")
            self.loginWindow.errorMessage.setVisible(False)
            self.loginWindow.close()       # Close the login window
            self.openInteractionWindow()  # Open the interaction window

        else:
            # Handle invalid login
            self.loginWindow.errorMessage.setText("Invalid Username or Password.")
            self.loginWindow.errorMessage.setVisible(True)

    def validateLogin(self, username, password):
        # This is a placeholder function for login validation
        # You should replace this with your actual validation logic
        # For example, checking against a database of registered users
        return username == "1" and password == "1"

    def openInteractionWindow(self):
        self.interactionWindow = interactionWindow()
        self.interactionWindow.show()
#======================================================================================

def main():
    app = QApplication(sys.argv)
    mainApp = mainApplication()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()