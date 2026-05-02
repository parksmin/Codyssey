import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    '''
    출력 값의 길이에 따라 폰트 크기를 자동 조절하고 
    소수점 6자리 반올림 기능을 포함한 계산기입니다.
    '''

    def __init__(self):
        super().__init__()
        self.current_value = '0'
        self.first_operand = None
        self.current_operator = None
        self.is_new_input = True
        self.max_float = sys.float_info.max
        
        # 폰트 조절을 위한 설정값
        self.base_font_size = 20
        self.min_font_size = 10
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Mars Mission Calculator Pro')
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()
        
        self.display = QLineEdit('0', self)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        # 초기 스타일 설정
        self.display.setStyleSheet(f'font-size: {self.base_font_size}px; border: none; background: #f0f0f0;')
        layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        for btn_text, *pos in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)
            button.clicked.connect(self.on_button_clicked)
            if len(pos) == 2:
                grid.addWidget(button, pos[0], pos[1])
            else:
                grid.addWidget(button, pos[0], pos[1], pos[2], pos[3])
                button.setFixedSize(130, 60)

        layout.addLayout(grid)
        self.setLayout(layout)

    def on_button_clicked(self):
        sender = self.sender().text()
        if sender.isdigit():
            self.append_number(sender)
        elif sender == '.':
            self.append_dot()
        elif sender == 'AC':
            self.reset()
        elif sender == '+/-':
            self.negative_positive()
        elif sender == '%':
            self.percent()
        elif sender in ['+', '-', '*', '/']:
            self.prepare_operation(sender)
        elif sender == '=':
            self.equal()

    def update_display(self):
        '''글자 수에 따라 폰트 크기를 조정하여 디스플레이 업데이트'''
        text_length = len(self.current_value)
        
        # 글자 수가 많아질수록 폰트 크기 축소 (기본 20px에서 최소 10px까지)
        if text_length > 10:
            new_size = max(self.min_font_size, self.base_font_size - (text_length - 10))
        else:
            new_size = self.base_font_size
            
        self.display.setFont(QFont('Arial', new_size))
        self.display.setText(self.current_value)

    def append_number(self, number):
        if self.is_new_input:
            self.current_value = number
            self.is_new_input = False
        else:
            if self.current_value == '0':
                self.current_value = number
            else:
                self.current_value += number
        self.update_display()

    def append_dot(self):
        if '.' not in self.current_value:
            self.current_value += '.'
            self.is_new_input = False
            self.update_display()

    def reset(self):
        self.current_value = '0'
        self.first_operand = None
        self.current_operator = None
        self.is_new_input = True
        self.update_display()

    def negative_positive(self):
        val = float(self.current_value)
        if val != 0:
            val = -val
        self.current_value = str(int(val) if val.is_integer() else val)
        self.update_display()

    def percent(self):
        val = float(self.current_value) / 100
        # 퍼센트 결과도 소수점 6자리 반올림 적용 가능성 고려
        self.current_value = str(round(val, 6))
        self.update_display()

    def prepare_operation(self, operator):
        self.first_operand = float(self.current_value)
        self.current_operator = operator
        self.is_new_input = True

    def equal(self):
        if self.current_operator is None:
            return

        try:
            second_operand = float(self.current_value)
            
            if self.current_operator == '+':
                result = self.first_operand + second_operand
            elif self.current_operator == '-':
                result = self.first_operand - second_operand
            elif self.current_operator == '*':
                result = self.first_operand * second_operand
            elif self.current_operator == '/':
                if second_operand == 0:
                    raise ZeroDivisionError('0으로 나눌 수 없습니다.')
                result = self.first_operand / second_operand

            if abs(result) > self.max_float:
                raise OverflowError('범위 초과')

            # 소수점 6자리 이하 반올림 처리
            if not result.is_integer():
                result = round(result, 6)
            
            # 정수형태인 경우 .0 제거
            self.current_value = str(int(result) if result == int(result) else result)
            
            self.first_operand = None
            self.current_operator = None
            self.is_new_input = True
            self.update_display()

        except ZeroDivisionError:
            self.display.setText('Error: Div/0')
            self.is_new_input = True
        except OverflowError:
            self.display.setText('Error: Overflow')
            self.is_new_input = True
        except Exception:
            self.display.setText('Error')
            self.is_new_input = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())