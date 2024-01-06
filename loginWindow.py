# Import necessary modules from PyQt6 for GUI development
from PyQt6.QtWidgets import *          
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# Import the 'tempWindow' class from the custom module 'baseWindow'
from baseWindow import tempWindow     

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

class loginWindow(tempWindow):                                 # Create a class 'loginWindow' that inherits from 'tempWindow'
    def __init__(self):                                        # Constructor to create an instance of the 'loginWindow' class
        super().__init__("Login", "background-color: black;")  # Call the constructor of the parent class to set attributes of the new class      
        font = QFont()                                         # This line creates an instance of the Qfont class in Pyqt, it will be used to control the font on this page type
        font.setPointSize(24)                                  # This line increase the font size to its max value of 24 for the login title 

        layout = QVBoxLayout()                                 # Creates an instance of the class QVBoxLayout, this will be used to manage how 'widgets' are placed on the login screen (Verticle)
        layout.addStretch()                                    # Adds the spaceing to the area above login to keep it balanced with the bottom spacing                                        

        title = QLabel("Login", self)                                       # Adds a label widget that will display the text login to the user
        title.setFont(font)                                                 # Sets the font attribute to the login text widget
        title.setStyleSheet("color: white;")                                # Makes the color of the text white so you can read it
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)     # Adds the title widget to the overall layout and aligns it in the center of the screen always

        # Create username and password input fields
        usernameInput = QLineEdit()                    # Create an input field for the username
        passwordInput = QLineEdit()                    # Create an input field for the password
        self.usernameInput = usernameInput             # Assign username_input as a class attribute
        self.passwordInput = passwordInput             # Assign password_input as a class attribute
        usernameInput.setPlaceholderText("Username")   # Set a placeholder text to provide a hint for the user 
        passwordInput.setPlaceholderText("Password")   # Set a placeholder text to provide a hint for the user 
        usernameInput.setStyleSheet("color: gray;")    # Set the text color of the input field's placeholder text to gray
        passwordInput.setStyleSheet("color: gray;")    # Set the text color of the input field's placeholder text to gray
        usernameInput.setFixedWidth(300)               # Set a fixed width of 300 pixels for the username input field
        usernameInput.setFixedHeight(25)               # Set a fixed height of 25 pixels for the username input field
        passwordInput.setFixedWidth(300)               # Set a fixed width of 300 pixels for the password input field
        passwordInput.setFixedHeight(25)               # Set a fixed height of 25 pixels for the password input field
        passwordInput.setEchoMode(QLineEdit.EchoMode.Password)

        # Add widgets to the layout with alignment
        layout.addWidget(usernameInput, alignment=Qt.AlignmentFlag.AlignCenter)    # Adds the username input widget to the layout and aligns it center
        layout.addWidget(passwordInput, alignment=Qt.AlignmentFlag.AlignCenter)    # Adds the password input widget and aligns it in the center

        self.errorMessage = QLabel("", self)
        self.errorMessage.setStyleSheet("color: red; font-size: 12px;")  # Set the text color to red and font size
        self.errorMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errorMessage.setVisible(False)  # Make it invisible initially
        layout.addWidget(self.errorMessage, alignment=Qt.AlignmentFlag.AlignCenter)

        submitButton = QPushButton("Submit", self)
        submitButton.setStyleSheet("background-color: white;")
        self.submitButton = submitButton  # Assign submit_button to a class attribute
        layout.addWidget(submitButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a stretchable space to push the input boxes to the bottom
        layout.addStretch() # Adds the spaceing to the area below password input to keep it balanced with the top spacing   

        # Set the layout for the main window
        container = QWidget()               # Create a QWidget called 'container' to hold the layout and widgets
        container.setLayout(layout)         # Set the layout of the container to the previously defined 'layout'
        self.setCentralWidget(container)    # Set 'container' as the central widget of the QMainWindow

