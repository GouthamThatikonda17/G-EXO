"""
=========================================================
Project G-EXO Desktop
Dark Theme
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

DARK_THEME = """

QMainWindow{

    background:#0F1115;

}

QWidget{

    background:#0F1115;

    color:white;

    font-family:Segoe UI;

    font-size:14px;

}

/* -------------------------------------------------- */
/* LABEL */
/* -------------------------------------------------- */

QLabel{

    color:white;

}

/* -------------------------------------------------- */
/* TEXT EDIT */
/* -------------------------------------------------- */

QTextEdit{

    background:#161A22;

    border:none;

    color:white;

    padding:15px;

    selection-background-color:#00BCD4;

}

/* -------------------------------------------------- */
/* LINE EDIT */
/* -------------------------------------------------- */

QLineEdit{

    background:#1B1F27;

    border:1px solid #2E3440;

    border-radius:10px;

    color:white;

    padding:10px;

}

QLineEdit:focus{

    border:1px solid #00BCD4;

}

/* -------------------------------------------------- */
/* BUTTON */
/* -------------------------------------------------- */

QPushButton{

    background:#00BCD4;

    color:black;

    border:none;

    border-radius:10px;

    padding:10px 20px;

    font-weight:bold;

}

QPushButton:hover{

    background:#29D7F3;

}

/* -------------------------------------------------- */
/* SCROLL BAR */
/* -------------------------------------------------- */

QScrollBar:vertical{

    background:#101418;

    width:10px;

}

QScrollBar::handle:vertical{

    background:#00BCD4;

    border-radius:5px;

}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical{

    height:0px;

}
"""