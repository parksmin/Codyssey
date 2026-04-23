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
    4칙 연산이 가능하도록 구현한다.
    '''

    def __init__(self):
        super().__init__()
        self.current_input = '0'
        self.expression = ''
        self.just_evaluated = False
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
        '''
        if value in '0123456789':
            self._input_number(value)
        elif value == '.':
            self._input_decimal()
        elif value in ('+', '−', '×', '÷'):
            self._input_operator(value)
        elif value == '=':
            self._calculate_result()
        elif value == 'AC':
            self._clear_all()
        elif value == '+/-':
            self._toggle_sign()
        elif value == '%':
            self._apply_percent()

        self.display.setText(self.current_input)

    def _input_number(self, value):
        '''
        숫자 입력 처리
        '''
        if self.just_evaluated:
            self.current_input = value
            self.expression = ''
            self.just_evaluated = False
            return

        if self.current_input == '0':
            self.current_input = value
        else:
            self.current_input += value

    def _input_decimal(self):
        '''
        소수점 입력 처리
        '''
        if self.just_evaluated:
            self.current_input = '0.'
            self.expression = ''
            self.just_evaluated = False
            return

        if '.' not in self.current_input:
            self.current_input += '.'

    def _input_operator(self, operator_symbol):
        '''
        연산자 입력 처리
        '''
        operator_map = {
            '+': '+',
            '−': '-',
            '×': '*',
            '÷': '/',
        }

        if self.just_evaluated:
            self.expression = self.current_input
            self.just_evaluated = False
        else:
            self.expression += self.current_input

        if self.expression and self.expression[-1] in '+-*/':
            self.expression = self.expression[:-1]

        self.expression += operator_map[operator_symbol]
        self.current_input = '0'

    def _calculate_result(self):
        '''
        수식을 계산하여 결과를 표시
        '''
        if self.just_evaluated:
            return

        full_expression = self.expression + self.current_input

        try:
            result = eval(full_expression, {'__builtins__': None}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.current_input = str(result)
            self.expression = ''
            self.just_evaluated = True
        except ZeroDivisionError:
            self.current_input = 'Error'
            self.expression = ''
            self.just_evaluated = True
        except Exception:
            self.current_input = 'Error'
            self.expression = ''
            self.just_evaluated = True

    def _clear_all(self):
        '''
        계산기 초기화
        '''
        self.current_input = '0'
        self.expression = ''
        self.just_evaluated = False

    def _toggle_sign(self):
        '''
        현재 숫자의 부호 변경
        '''
        if self.current_input == '0' or self.current_input == 'Error':
            return

        if self.current_input.startswith('-'):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = '-' + self.current_input

    def _apply_percent(self):
        '''
        현재 숫자를 백분율 값으로 변환
        '''
        if self.current_input == 'Error':
            return

        try:
            value = float(self.current_input) / 100
            if value.is_integer():
                value = int(value)
            self.current_input = str(value)
        except ValueError:
            self.current_input = 'Error'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = CalculatorUI()
    calculator.show()
    sys.exit(app.exec_())