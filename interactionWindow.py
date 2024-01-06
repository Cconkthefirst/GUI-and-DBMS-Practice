from PyQt6.QtWidgets import *       # Import necessary modules
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from baseWindow import tempWindow   # Import custom modules
from databseLogic import *

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

class interactionWindow(tempWindow):                                 # Create a class 'interactionWindow' that inherits from 'tempWindow'
    def __init__(self):                                              # Constructor for the class
        super().__init__("Interaction", "background-color: black;")  # Call the constructor of the parent class
        # Close when click home and open a new wkindow
        #make sure we dont have to be taken back to the login screen
#================================================================================================================
#NOTICE:                                                                                                        |
#-------                                                                                                        |
# The code inside the line of equal signs builds the actual structure and style of the interaction window,      |
# it has nothing to do with handling the fucntionality of certain elements on the screen, but it may            |
# refrenece some functioins on the interavite components of the window. All the functions to handle user        |
# interaction are built out below the last big dividing line like seen above.                                   |
#================================================================================================================
        font = QFont()                              # Create a QFont object
        font.setPointSize(24)                       # Set the font size

        self.label = QLabel("Welcome.")             # Create a QLabel with the text "Welcome."
        self.label.setFont(font)                    # Set the font of the label using the previously defined QFont object
        self.label.setStyleSheet("color: white;")   # Set the text color of the label to white

        self.directions = QLabel (f"You will be interacting with the system by clicking a button below.\n Update: Allows you to change entries in Database.\n Analysis: Allows you to specify what data you want to see from database.\n Entry: Allows you to enter new records into the database or create entirely new tables.\n")  
        font.setPointSize(8)                                 # Set the font size to 8
        self.directions.setFont(font)                        # Set the font of the label using the modified QFont object
        self.directions.setStyleSheet("color: gray;")        # Set the text color of the label to gray

        layout = QGridLayout()                               # Create a vertical layout

        self.input_box_layout = QHBoxLayout()                # Create a QHBoxLayout for input boxes
        self.boxes_added = False                             # Flag to track whether input boxes have been added
        self.current_table = None

        # Create a QTextEdit for displaying query results
        self.query_results_area = QTextEdit()                                                               # Create a QTextEdit widget for displaying text
        self.query_results_area.setStyleSheet("color: gray;")                                               # Set the text color to gray
        self.query_results_area.setReadOnly(True)                                                           # Make the text area read-only
        self.query_results_area.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)                         # Wrap lines to fit the width of the widget
        self.query_results_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)           # Disable the vertical scrollbar by default
        self.query_results_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)         # Disable the horizontal scrollbar by default
        self.query_results_area.setFrameStyle(0)                                                            # Set the frame style to 0 (no frame)
        self.query_results_area.enterEvent = lambda event: self.show_scrollbar(True)                        # Show the vertical scrollbar when the mouse enters the widget
        self.query_results_area.leaveEvent = lambda event: self.show_scrollbar(False)                       # Hide the vertical scrollbar when the mouse leaves the widget

        # Create a QToolBar for adding buttons
        self.toolbar = QToolBar("My main toolbar")                                                           # Create a QToolBar with the given name
        self.toolbar.setMovable(False)                                                                       # Make the toolbar non-movable
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)                         # Set the tool button style to display text beside the icon
        toolbar_size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)        # Set the size hint for the toolbar to take up 20% of the screen width
        toolbar_size_policy.setHorizontalStretch(0.2)                                                        # Set the horizontal stretch factor to 20% of the available space
        self.toolbar.setSizePolicy(toolbar_size_policy)

        self.updateListArea = QWidget()
        self.updateListArea.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        self.entryListArea = QWidget()
        self.entryListArea.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        self.analyzeListArea = QWidget()
        self.analyzeListArea.setStyleSheet("background-color: rgba(0, 0, 0, 100);")


        # Create a QVBoxLayout for the toolbarListArea
        #  self.toolbarListLayout = QVBoxLayout(self.toolbarListArea)

        # Create and configure the first button
        self.button1 = QToolButton()                                                   # Create a QToolButton for the first button
        self.button1.setText("Update")                                                 # Set the button text to "Update"
        self.button1.setStyleSheet("background-color: white; border-radius: 10px;")    # Set the style sheet to define the appearance of the button
        self.button1.clicked.connect(self.updateButtonClick)

        # Create and configure the second button
        self.button2 = QToolButton()                                                   # Create a QToolButton for the second button
        self.button2.setText("Analyze")                                                # Set the button text to "Analyze"
        self.button2.setStatusTip("The analysis button")                               # Set the status tip for the button
        self.button2.setStyleSheet("background-color: white; border-radius: 10px;")    # Set the style sheet to define the appearance of the button
        self.button2.clicked.connect(self.analyzeButtonClick)

        # Create and configure the third button
        self.button3 = QToolButton()                                                   # Create a QToolButton for the third button
        self.button3.setText("Entry")                                                  # Set the button text to "Entry"
        self.button3.setStatusTip("The data entry button")                             # Set the status tip for the button
        self.button3.setStyleSheet("background-color: white; border-radius: 10px;")    # Set the style sheet to define the appearance of the button
        self.button3.clicked.connect(self.entryButtonClick)

        # Create and configure the home button
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.home_button.clicked.connect(self.goHome)

        # Set the size policy for the spacers
        spacer_size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a spacer widget to add space on the left side
        self.left_spacer = QWidget() 
        self.left_spacer.setSizePolicy(spacer_size_policy)

        # Create a spacer widget to add space on the right side
        self.right_spacer = QWidget() 
        self.right_spacer.setSizePolicy(spacer_size_policy)

        # Add widgets to the toolbar
        self.toolbar.addWidget(self.left_spacer)  # Add a spacer on the left side
        self.toolbar.addWidget(self.button1)      # Add button1 to the toolbar
        self.toolbar.addSeparator()               # Add a flexible separator
        self.toolbar.addWidget(self.button2)      # Add button2 to the toolbar
        self.toolbar.addSeparator()               # Add another flexible separator
        self.toolbar.addWidget(self.button3)      # Add button3 to the toolbar
        self.toolbar.addWidget(self.right_spacer) # Add a spacer on the right side

        # Create a spacer widget to add space at the bottom
        self.spacer = QWidget()                                                                 # Create a QWidget for spacing
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)   # Set the size policy to expanding, allowing it to take up available space

        # Add widgets to the layout
        # layout.addLayout(reset_layout)
        layout.addWidget(self.home_button, 0,1,1,5)# Add the home button to the layout
        layout.addWidget(self.label, 0,0,1,1)                                                    # Add the welcome message label to the layout
        layout.addWidget(self.directions, 1,0,1,1)                                               # Add the instructional label to the layout
        layout.addLayout(self.input_box_layout, 2,0,1,1)
        layout.addWidget(self.query_results_area, 3,0,1,3)                                       # Add the text area for query results to the layout
        layout.addWidget(self.updateListArea, 3,0,1,2)
        layout.addWidget(self.entryListArea, 3,0,1,2)
        layout.addWidget(self.analyzeListArea, 3,0,1,2)
        # layout.addWidget(self.spacer)                                                          # Add the spacer widget at the bottom to the layout
        layout.addWidget(self.toolbar, 4,0,1,1)                                                  # Add the toolbar to the layout

        self.updateListArea.hide()
        self.entryListArea.hide()
        self.analyzeListArea.hide()
        self.setupViews()

        # Create a widget and set the layout
        widget = QWidget()                  # Create a QWidget to hold the layout
        widget.setLayout(layout)            # Set the layout for the widget
        self.setCentralWidget(widget)       # Set the central widget of the main window to the configured widget        
        self.setStatusBar(QStatusBar(self)) # Set the status bar
#================================================================================================================

#================================================================================================================
#NOTICE:                                                                                                         |
#-------                                                                                                         |
# Everything below the line of equal marks are the functions that handle the                                     |
# interaction between page elements and the database. Note that some functions here                              |
# will reference others that have been built ot in the databaseLogic file, to see                                |
# those, please go to that file.                                                                                 |
#================================================================================================================

#================================================================================================================
#Helper Functions for genral use:                                                                                |
#================================================================================================================
    # Show or hide the vertical scrollbar based on the 'show' parameter
    def show_scrollbar(self, show):
        if show:
            self.query_results_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        else:
            self.query_results_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    #Query Format Filter button Functions:
    def clearInputBoxes(self):
        # Remove all input boxes from the layout
        for i in reversed(range(self.input_box_layout.count())):
            self.input_box_layout.itemAt(i).widget().setParent(None)
        self.boxes_added = False

    def inputboxCreator(self, box):
        box.setStyleSheet("color: gray;")                   # Set the text color to gray
        box.setFixedWidth(300)                              # Set a fixed width for the input field
        box.setFixedHeight(30)                              # Set a fixed height for the input field

    def goHome(self):
        self.clearInputBoxes()
        self.query_results_area.clear()
        self.updateListArea.hide()
        self.entryListArea.hide()
        self.analyzeListArea.hide()
        self.enableAllButtons()

    def setupViews(self):
        self.setupdateView()
        self.setentryView()
        self.setAnalyzeView()

    def setupdateView(self):
        table_list = fetchAllTables()
        # Clear the existing content in the toolbarListArea
        toolbar_layout = self.updateListArea.layout()
        if toolbar_layout:
            for i in reversed(range(toolbar_layout.count())):
                toolbar_layout.itemAt(i).widget().setHidden(True)

        # Create a QVBoxLayout for the list and title
        layout = QVBoxLayout()

        # Add a title label with underline
        title_label = QLabel("Tables in Database:")
        title_label.setStyleSheet("color: white; font-size: 16px; text-decoration: underline;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        list_widget = QListWidget()
        list_widget.setFrameShape(QFrame.Shape.NoFrame)

        # Populate the QListWidget with table names
        for table in table_list:
            item = QListWidgetItem(table)
            item.setTextAlignment(0x0020)               # Align text to the center
            item.setForeground(QColor(255, 255, 255))   # White text color
            item.setBackground(QColor(0, 0, 0))         # Example: black background
            list_widget.addItem(item)

        list_widget.itemClicked.connect(lambda item: self.onUpdatefTableClicked(item.text()))        # Connect the itemClicked signal to pass the table name


        layout.addWidget(list_widget, alignment=Qt.AlignmentFlag.AlignCenter)                        # Add the list widget to the layout

        self.updateListArea.setLayout(layout)                                                        # Set the layout for the toolbarListArea

    def setentryView(self):
        table_list = fetchAllTables()
        # Create and configure the "Create New Table" button
        self.CreateNewTable = QPushButton("Create New Table")
        self.CreateNewTable.setStyleSheet("background-color: white; border-radius: 10px;")
        self.CreateNewTable.clicked.connect(self.onCreateNewTableClick)

        # Create a QVBoxLayout to hold the list of tables and title
        layout = QVBoxLayout()

        # Add a title label with underline
        title_label = QLabel("Tables in Database:")
        title_label.setStyleSheet("color: white; font-size: 16px; text-decoration: underline;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center-align and underline the title

        list_widget = QListWidget()  # Create a QListWidget to display the list of tables
        list_widget.itemClicked.connect(self.onTableClicked)  # Set up a signal to connect to the onTableClicked function
        list_widget.setFrameShape(QFrame.Shape.NoFrame)  # Remove the border from the QListWidget

        # Populate the QListWidget with table names
        for table in table_list:
            item = QListWidgetItem(table)
            item.setTextAlignment(0x0020)  # Align text to the center
            item.setForeground(QColor(255, 255, 255))  # White text color
            item.setBackground(QColor(0, 0, 0))  # Example: black background
            list_widget.addItem(item)  # Add the item to the QListWidget

        layout.addWidget(list_widget, alignment=Qt.AlignmentFlag.AlignCenter)  # Center-align the QListWidget
        layout.addWidget(self.CreateNewTable, alignment=Qt.AlignmentFlag.AlignCenter)  # Add the "Create New Table" button to the layout
        # layout.addLayout(create_button_layout)  # Add the button layout to the main layout

        self.entryListArea.setLayout(layout)  # Set the layout for the self.entryListArea

    def setAnalyzeView(self):
        qListlayout = QVBoxLayout()

        # Create a list widget to display predefined queries
        ListTitle = QLabel("Available Queries:")
        ListTitle.setStyleSheet("color: white; font-size: 16px; text-decoration: underline;")  # Set title label styling
        qListlayout.addWidget(ListTitle, alignment=Qt.AlignmentFlag.AlignCenter)  # Center-align and underline the title

        querryList = QListWidget()
        querryList.itemClicked.connect(self.handlePriorityQuerry)
        querryList.setFrameShape(QFrame.Shape.NoFrame)

        # Populate the list widget with predefined queries
        for query_info in predefined_queries:
            item = QListWidgetItem(query_info["name"])
            item.setForeground(QColor(255, 255, 255))
            item.setBackground(QColor(0, 0, 0))
            querryList.addItem(item)

        # Add the list widget to the layout
        qListlayout.addWidget(querryList, alignment=Qt.AlignmentFlag.AlignCenter)
        self.analyzeListArea.setLayout(qListlayout)

    def enableAllButtons(self):
        # Enable all buttons in the toolbar
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def disableButtonsExcept(self, current_button):
        # Disable all buttons in the toolbar except the current button
        all_buttons = [self.button1, self.button2, self.button3]
        for button in all_buttons:
            if button != current_button:
                button.setEnabled(False)
#================================================================================================================

#================================================================================================================
#UDATE BUTTON FUNCTIONALITY:
#================================================================================================================
    def updateButtonClick(self):
        self.updateListArea.show()
        self.disableButtonsExcept(self.button1)

    def onUpdatefTableClicked(self, table_name):
        # Hide the updateListArea
        self.updateListArea.hide()

        # Set the current table name
        self.current_table = table_name

        # Display the selected table in the query result area
        self.displayTableFromInput(self.current_table)
        
        # Create input boxes for the update
        self.IDSelect = QLineEdit()
        self.IDSelect.setPlaceholderText("ID/Key")
        self.attribute_input = QLineEdit()
        self.attribute_input.setPlaceholderText("Select Attribute")
        self.new_data_input = QLineEdit()
        self.new_data_input.setPlaceholderText("Enter Change")

        self.input_box_layout.addWidget(self.IDSelect)
        self.input_box_layout.addWidget(self.attribute_input)
        self.input_box_layout.addWidget(self.new_data_input)

        self.inputboxCreator(self.IDSelect)
        self.inputboxCreator(self.attribute_input)
        self.inputboxCreator(self.new_data_input)
        self.boxes_added = True

        self.new_data_input.returnPressed.connect(self.sendUpdateRequest)

    def displayTableFromInput(self, input_widget):
        self.query_results_area.clear()  # Clear existing content

        # If the input_widget is a string, use it as the table name directly
        if isinstance(input_widget, str):
            table_name = input_widget
        elif isinstance(input_widget, QLineEdit):
            # If the input_widget is a QLineEdit, get the text from it
            table_name = input_widget.text()
        else:
            # Handle other cases if needed
            print("Invalid input_widget type")

        if table_name:
            result = displayTable(table_name)
            self.query_results_area.setHtml(f'<div style="border: 1px solid white;">{result}</div>')

    def sendUpdateRequest(self):
        if self.attribute_input.text():
            tableName = self.current_table
            key = self.IDSelect.text()
            oldAttribute = self.attribute_input.text()
            newAttributeInfo = self.new_data_input.text()

            # Update the database
            updateDatabase(tableName, key, oldAttribute, newAttributeInfo)

            # Display the updated table
            updatedTable = displayTable(tableName)
            self.query_results_area.setHtml(f'<div style="border: 1px solid white;">{updatedTable}</div>')
        else:
            print("Please enter the required information.")
#================================================================================================================

#================================================================================================================
#ENTRY BUTTON FUNCTIONALITY:
#================================================================================================================
    def entryButtonClick(self):
        self.entryListArea.show()
        self.CreateNewTable.show()
        self.query_results_area.clear()  # Clear the existing content in the query results area
        table_list = fetchAllTables()  # Fetch a list of all tables in the database
        self.disableButtonsExcept(self.button3)

    def onTableClicked(self, item):
        toolbar_layout = self.entryListArea.layout()
        self.entryListArea.hide()
        self.CreateNewTable.setHidden(True)
        if item:
            table_name = item.text()
            self.current_table = table_name
            self.displayTableFromInput(table_name)
            self.newEntry = QLineEdit()
            self.newEntry.setPlaceholderText("Enter by Row Order:(EX: Name, leave blank empty, Number, ...)")
            self.newEntry.returnPressed.connect(self.processNewEntry)
            self.inputboxCreator(self.newEntry)
            upperlayout = self.input_box_layout
            upperlayout.addWidget(self.newEntry)
            self.boxes_added = True

    def processNewEntry(self):
        try:
            # Take the text from the entry box
            entry_text = self.newEntry.text()

            # Call the database logic function to handle entry
            enterData(entry_text, self.current_table)

            # Display a success message to the user
            print("Entry successful!")

            # Reprint the table to the screen with updated info
            self.displayTableFromInput(self.current_table)

        except Exception as e:
            # Display an error message to the user
            print(f"Error during entry: {str(e)}")


    def onCreateNewTableClick(self):
        # # Hide the table list, the table list title, and the "Create New Table" button
        # self.query_results_area.clear()
        # lowerlayout = self.query_results_area.layout()
        # lowerlayout.itemAt(0).widget().setHidden(True)  # Assuming the title label is the first item in the layout
        # lowerlayout.itemAt(1).widget().setHidden(True)  # Assuming the list widget is the second item in the layout
        # self.CreateNewTable.setHidden(True)
        self.entryListArea.hide()

        self.enterSchema = QLineEdit()
        self.enterSchema.setPlaceholderText("Enter Schema: TableName(attribute1-datatype-, attribute2-datatype-, ...)")
        self.enterSchema.returnPressed.connect(self.createNewTable)
        self.inputboxCreator(self.enterSchema)
        self.input_box_layout.addWidget(self.enterSchema)
        

        #i need to hide the table list and the table list title and the create new table buttoon whe nthis fucntion is called
        
    def createNewTable(self):
        #this is called when the create new tbale button is pressed
        #On press the user will be presented with a Qlineedit object to input schema into
        #The box will appear in the input box area
        #Schema format goes TableName(attribute1, attribute2, ...)
        #When the user presses enter after entering a schema add the table to the database
        #After the table is added to the database, we need to prove it to the user
        #TO do that i want to show a list of all the tables in db
        newTableSchema = self.enterSchema.text()
        newTableSchema.strip()

        try:
            createTable(newTableSchema)
            print("It worked yay")
            # self.clearInputBoxes()
            # self.goHome()
        except Exception as e:
            # Display an error message to the user
            print(f"Error creating new table: {str(e)}")

    def showNewTable(self):
        return 0
#================================================================================================================

#================================================================================================================
#ANALYZE BUTTON FUNCTIONALITY:
#================================================================================================================
    def analyzeButtonClick(self):
        self.analyzeListArea.show()
        self.query_results_area.clear()
        self.disableButtonsExcept(self.button2)

    def handlePriorityQuerry(self, item):
        try:
            # Clear the toolbarListArea content
            toolbar_layout = self.analyzeListArea.layout()
            if toolbar_layout:
                while toolbar_layout.count():
                    toolbar_layout.takeAt(0).widget().setHidden(True)

            selectedQuery = item.text()
            tableHtml = runPredefinedQuery(selectedQuery)

            # Check if tableHtml is not None before displaying it
            if tableHtml is not None:
                # Show the query results area and set the HTML content
                self.query_results_area.show()
                self.query_results_area.setHtml(tableHtml)
            else:
                print("Error: Table HTML is None.")

        except Exception as e:
            print(f"Error handling priority query: {e}")
#================================================================================================================
