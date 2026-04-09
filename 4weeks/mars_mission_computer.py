import json
import random
import time
import datetime

try:
    import msvcrt
    IS_WINDOWS = True
except ImportError:
    import select
    import sys
    import termios
    import tty
    IS_WINDOWS = False


class DummySensor:
    '''
    화성 기지의 환경 수치를 무작위로 생성하고 관리하며,
    조회 시 로그를 파일에 기록하는 더미 센서 클래스.
    '''

    def __init__(self):
        '''
        환경 변수를 저장할 사전(dict) 객체를 멤버로 초기화한다.
        '''
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }

    def set_env(self):
        '''
        각 환경 항목에 대해 지정된 범위 내의 랜덤 값을 생성하여 저장한다.
        '''
        self.env_values['mars_base_internal_temperature'] = round(
            random.uniform(18, 30), 2
        )
        self.env_values['mars_base_external_temperature'] = round(
            random.uniform(0, 21), 2
        )
        self.env_values['mars_base_internal_humidity'] = round(
            random.uniform(50, 60), 2
        )
        self.env_values['mars_base_external_illuminance'] = round(
            random.uniform(500, 715), 2
        )
        self.env_values['mars_base_internal_co2'] = round(
            random.uniform(0.02, 0.1), 4
        )
        self.env_values['mars_base_internal_oxygen'] = round(
            random.uniform(4, 7), 2
        )

    def get_env(self):
        '''
        환경 데이터를 반환하고, 동시에 mission_log.txt 파일에
        날짜와 환경 수치를 기록한다.
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_msg = (
            f'[{now}] '
            f'내부온도: {self.env_values["mars_base_internal_temperature"]}°C, '
            f'외부온도: {self.env_values["mars_base_external_temperature"]}°C, '
            f'내부습도: {self.env_values["mars_base_internal_humidity"]}%, '
            f'외부광량: {self.env_values["mars_base_external_illuminance"]}W/m2, '
            f'CO2농도: {self.env_values["mars_base_internal_co2"]}%, '
            f'산소농도: {self.env_values["mars_base_internal_oxygen"]}%\n'
        )

        try:
            with open('mission_log.txt', mode='a', encoding='utf-8') as file:
                file.write(log_msg)
        except OSError as error:
            print(f'로그 기록 중 오류 발생: {error}')

        return self.env_values


class MissionComputer:
    '''
    더미 센서에서 생성한 환경 데이터를 받아 저장하고,
    JSON 형태로 주기적으로 출력하는 미션 컴퓨터 클래스.
    '''

    def __init__(self):
        '''
        환경 데이터를 저장할 사전(dict) 객체와
        5분 평균 계산용 기록 리스트를 초기화한다.
        '''
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        self.env_history = []
        self.stop_key = 'q'

    def check_stop_key(self):
        '''
        종료 키 입력 여부를 확인한다.
        q 키가 입력되면 True를 반환한다.
        '''
        if IS_WINDOWS:
            if msvcrt.kbhit():
                pressed_key = msvcrt.getwch()
                if pressed_key.lower() == self.stop_key:
                    return True
            return False

        file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)

        try:
            tty.setcbreak(file_descriptor)
            readable, _, _ = select.select([sys.stdin], [], [], 0)
            if readable:
                pressed_key = sys.stdin.read(1)
                if pressed_key.lower() == self.stop_key:
                    return True
        finally:
            termios.tcsetattr(
                file_descriptor,
                termios.TCSADRAIN,
                old_settings
            )

        return False

    def print_five_minute_average(self):
        '''
        최근 5분 동안의 환경값 평균을 계산하여 JSON 형태로 출력한다.
        5초마다 1번 측정하므로 60개 데이터가 모이면 5분 평균이다.
        '''
        if not self.env_history:
            return

        average_values = {}

        for key in self.env_history[0]:
            total = 0.0
            for item in self.env_history:
                total += item[key]
            average_values[key] = round(total / len(self.env_history), 4)

        print('\n--- 최근 5분 평균 환경 정보 ---')
        print(json.dumps(average_values, indent=4, ensure_ascii=False))
        print()

        self.env_history.clear()

    def get_sensor_data(self):
        '''
        센서 값을 가져와 env_values에 저장하고,
        JSON 형태로 화면에 출력한다.
        위 동작을 5초에 한 번씩 반복한다.

        보너스 기능:
        - q 키 입력 시 반복을 중단하고 'Sytem stoped....'를 출력한다.
        - 5분마다 평균 환경값을 별도로 출력한다.
        '''
        count = 0

        print('환경 데이터 출력을 시작합니다.')
        print('종료하려면 q 키를 누르세요.\n')

        while True:
            ds.set_env()
            self.env_values = ds.get_env()

            print('--- 화성 기지 환경 정보 ---')
            print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
            print()

            self.env_history.append(self.env_values.copy())
            count += 1

            if count % 60 == 0:
                self.print_five_minute_average()

            for _ in range(5):
                if self.check_stop_key():
                    print('Sytem stoped....')
                    return
                time.sleep(1)


ds = DummySensor()
RunComputer = MissionComputer()


if __name__ == '__main__':
    RunComputer.get_sensor_data()