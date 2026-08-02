"""
=========================================================
Project G-EXO Desktop
Main Window
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
)

from core.dispatcher import Dispatcher
from core.request import Request

from widgets.top_bar import TopBar
from widgets.sidebar import Sidebar
from widgets.chat_area import ChatArea
from widgets.message_input import MessageInput


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.dispatcher = Dispatcher()

        self.setWindowTitle("G-EXO")

        self.resize(1200, 750)

        self.setup_ui()

        self.setup_connections()

        self.chat_area.add_message(

            "G-EXO",

            "Welcome to G-EXO. How can I help you today?"

        )

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout()

        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.setSpacing(0)

        central_widget.setLayout(root_layout)

        self.sidebar = Sidebar()

        root_layout.addWidget(self.sidebar)

        right_widget = QWidget()

        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.setSpacing(0)

        right_widget.setLayout(right_layout)

        root_layout.addWidget(right_widget)

        self.top_bar = TopBar()

        right_layout.addWidget(self.top_bar)

        self.chat_area = ChatArea()

        right_layout.addWidget(self.chat_area)

        self.message_input = MessageInput()

        right_layout.addWidget(self.message_input)

    def setup_connections(self):

        self.message_input.send_button.clicked.connect(

            self.send_message

        )

        self.message_input.input.returnPressed.connect(

            self.send_message

        )

    def send_message(self):

        message = self.message_input.input.text().strip()

        if not message:

            return

        self.chat_area.add_message(

            "You",

            message,

        )

        request = Request(

            message=message,

            source="desktop",

        )

        response = self.dispatcher.dispatch(

            request

        )

        self.chat_area.add_message(

            "G-EXO",

            response.message,

        )

        self.message_input.input.clear()