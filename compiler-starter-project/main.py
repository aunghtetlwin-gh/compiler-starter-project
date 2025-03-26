import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLCDNumber

from components.lexica import MyLexer
from components.parsers import MyParser
from components.memory import Memory

class MainWindow(QMainWindow):

    # Do this for intellisense
    button_0: QPushButton        # 0
    button_1: QPushButton        # 1
    button_2: QPushButton        # 2
    button_3: QPushButton        # 3
    button_4: QPushButton        # 4
    button_5: QPushButton        # 5
    button_6: QPushButton        # 6
    button_7: QPushButton        # 7
    button_8: QPushButton        # 8
    button_9: QPushButton        # 9
    button_plus: QPushButton     # +
    button_star: QPushButton     # *
    button_equal: QPushButton    # =
    button_clear: QPushButton    # Clear

    input_text:QLineEdit         # Prefix input
    output_lcd:QLCDNumber        # Output Answer
    output_infix: QLineEdit      # Infix output

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main.ui", self)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: white;
                font-size: 18px;
            }
            
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #4C566A;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 18px;
            }
            
            QPushButton:hover {
                background-color: #5E81AC;
            }
            
            QPushButton:pressed {
                background-color: #88C0D0;
            }

            QLineEdit {
                background-color: #3B4252;
                color: white;
                border: 2px solid #81A1C1;
                border-radius: 8px;
                padding: 6px;
                font-size: 18px;
            }

            QLCDNumber {
                background-color: black;
                border: 2px solid #D8DEE9;
                border-radius: 8px;
            }
        """)

        #### Binding button to function ####
        # self.button_0.clicked.connect(lambda: self.push("0"))   
        self.button_1.clicked.connect(lambda: self.push("1"))
        self.button_2.clicked.connect(lambda: self.push("2"))
        self.button_3.clicked.connect(lambda: self.push("3"))
        self.button_4.clicked.connect(lambda: self.push("4"))
        self.button_5.clicked.connect(lambda: self.push("5"))
        self.button_6.clicked.connect(lambda: self.push("6"))
        self.button_7.clicked.connect(lambda: self.push("7"))
        self.button_8.clicked.connect(lambda: self.push("8"))
        self.button_9.clicked.connect(lambda: self.push("9"))

        self.button_plus.clicked.connect(lambda: self.push("+"))
        self.button_star.clicked.connect(lambda: self.push("*"))
        self.button_equal.clicked.connect(self.push_equal)
        self.button_clear.clicked.connect(self.clear)
        self.output_infix.setReadOnly(True)

    # def push_1(self):
    #     current_text:str = self.input_text.text()
    #     self.input_text.setText(f"{current_text}1")
    
    def push(self, text:str):
        current_text:str = self.input_text.text()
        self.input_text.setText(f"{current_text}{text}")

    def clear(self):
        """Clear all input and output fields."""
        self.input_text.setText("")       # Clear prefix input
        self.output_lcd.display(0)       # Reset answer display
        self.output_infix.setText("")       # Clear infix output
        # self.output_postfix.setText("")     # Clear postfix output
    
    def push_equal(self):
        print("Calculate")
        lexer = MyLexer()
        parser = MyParser()
        memory = Memory()

        input_text = self.input_text.text()
        tokens = lexer.tokenize(input_text)  # Convert input into tokens
        result = parser.parse(tokens)  # Get result only

        self.output_lcd.display(result.value)  # Show the result in LCD
        self.output_infix.setText(str(result))  # Show the converted infix expression

        # Debugging
        print(type(result))
        print("Infix Expression:", (str(result)))
        print(memory)

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()