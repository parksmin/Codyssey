import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculatorUI(QWidget):
    '''
    아이폰 계산기와 유사한 형태의 UI를 구성하는 클래스
    계산 기능은 구현하지 않고 버튼 입력만 화면에 표시한다.
    '''

    def __init__(self):
        super().__init__()
        self.current_input = '0'
        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        '''
        기본 윈도우 설정
        '''
        self.setWindowTitle('Calculator')
        self.setFixedSize(360, 640)
        self.setStyleSheet('background-color: black;')

    def _setup_ui(self):
        '''
        계산기 전체 UI 구성
        '''
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 20)
        main_layout.setSpacing(12)

        top_spacer = QHBoxLayout()
        top_spacer.addStretch()
        main_layout.addLayout(top_spacer)

        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFixedHeight(120)
        self.display.setFont(QFont('Arial', 36, QFont.Light))
        self.display.setStyleSheet(
            'color: white; background-color: black; padding-right: 12px;'
        )
        main_layout.addWidget(self.display)

        button_layout = QGridLayout()
        button_layout.setSpacing(12)

        buttons = [
            [('AC', 'function'), ('+/-', 'function'), ('%', 'function'), ('÷', 'operator')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('×', 'operator')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('−', 'operator')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operator')],
        ]

        for row_index, row_buttons in enumerate(buttons):
            for col_index, (text, button_type) in enumerate(row_buttons):
                button = self._create_button(text, button_type)
                button_layout.addWidget(button, row_index, col_index)

        zero_button = self._create_button('0', 'number', wide=True)
        decimal_button = self._create_button('.', 'number')
        equal_button = self._create_button('=', 'operator')

        button_layout.addWidget(zero_button, 4, 0, 1, 2)
        button_layout.addWidget(decimal_button, 4, 2)
        button_layout.addWidget(equal_button, 4, 3)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _create_button(self, text, button_type, wide=False):
        '''
        버튼 생성 및 스타일 적용
        '''
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setFont(QFont('Arial', 20))
        button.setFixedHeight(72)

        if wide:
            button.setFixedWidth(156)
            button.setStyleSheet(
                'QPushButton {'
                'background-color: #333333;'
                'color: white;'
                'border: none;'
                'border-radius: 36px;'
                'padding-left: 28px;'
                'text-align: left;'
                '}'
                'QPushButton:pressed {'
                'background-color: #4a4a4a;'
                '}'
            )
        else:
            button.setFixedSize(72, 72)
            button.setStyleSheet(self._get_button_style(button_type))

        button.clicked.connect(
            lambda checked, value=text: self._handle_button_click(value)
        )
        return button

    def _get_button_style(self, button_type):
        '''
        버튼 종류에 따라 스타일 반환
        '''
        if button_type == 'function':
            return (
                'QPushButton {'
                'background-color: #a5a5a5;'
                'color: black;'
                'border: none;'
                'border-radius: 36px;'
                '}'
                'QPushButton:pressed {'
                'background-color: #c7c7c7;'
                '}'
            )

        if button_type == 'operator':
            return (
                'QPushButton {'
                'background-color: #f1a33c;'
                'color: white;'
                'border: none;'
                'border-radius: 36px;'
                '}'
                'QPushButton:pressed {'
                'background-color: #f6bd73;'
                '}'
            )

        return (
            'QPushButton {'
            'background-color: #333333;'
            'color: white;'
            'border: none;'
            'border-radius: 36px;'
            '}'
            'QPushButton:pressed {'
            'background-color: #4a4a4a;'
            '}'
        )

    def _handle_button_click(self, value):
        '''
        버튼 입력 이벤트 처리
        숫자와 기호를 화면에 표시한다.
        실제 계산은 수행하지 않는다.
        '''
        if value == 'AC':
            self.current_input = '0'
        elif self.current_input == '0':
            self.current_input = value
        else:
            self.current_input += value

        self.display.setText(self.current_input)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = CalculatorUI()
    calculator.show()
    sys.exit(app.exec_())