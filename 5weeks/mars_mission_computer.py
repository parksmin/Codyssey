import json
import random
import time


try:
    import msvcrt

    WINDOWS_ENV = True
except ImportError:
    import select
    import sys
    import termios
    import tty

    WINDOWS_ENV = False


class DummySensor:
    '''
    화성 기지의 환경 값을 임의로 생성하는 더미 센서 클래스
    '''

    def __init__(self):
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
        지정된 범위 내에서 랜덤한 환경 값을 생성하여 저장한다.
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
        현재 환경 값을 반환한다.
        '''
        return self.env_values


class MissionComputer:
    '''
    더미 센서의 값을 받아 화성 기지의 환경 정보를 출력하는 미션 컴퓨터 클래스
    '''

    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        self.history = []
        self.stop_key = 'q'

    def _copy_sensor_values(self):
        '''
        더미 센서의 값을 가져와 env_values에 저장한다.
        '''
        sensor_data = ds.get_env()
        self.env_values = dict(sensor_data)

    def _print_env_values(self):
        '''
        env_values를 JSON 형태로 출력한다.
        '''
        print(json.dumps(self.env_values, indent=4))

    def _save_history(self):
        '''
        현재 env_values를 평균 계산을 위해 history에 저장한다.
        '''
        self.history.append(dict(self.env_values))

    def _print_five_minute_average(self):
        '''
        5분 동안 수집한 데이터(5초 간격 60개)의 평균을 출력한다.
        '''
        if not self.history:
            return

        average_values = {}
        keys = self.history[0].keys()

        for key in keys:
            total = 0.0
            for item in self.history:
                total += item[key]
            average_values[key] = round(total / len(self.history), 4)

        print('\n=== 5분 평균 환경 값 ===')
        print(json.dumps(average_values, indent=4))
        print()

        self.history.clear()

    def _check_stop_key(self):
        '''
        특정 키 입력 여부를 확인한다.
        q를 입력하면 반복을 종료한다.
        '''
        if WINDOWS_ENV:
            if msvcrt.kbhit():
                pressed_key = msvcrt.getwch()
                if pressed_key.lower() == self.stop_key:
                    print('Sytem stoped....')
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
                    print('Sytem stoped....')
                    return True
        finally:
            termios.tcsetattr(
                file_descriptor,
                termios.TCSADRAIN,
                old_settings,
            )

        return False

    def get_sensor_data(self):
        '''
        센서 값을 5초마다 가져와 env_values에 저장하고,
        JSON 형태로 출력한다.
        보너스:
        - q 키 입력 시 반복 종료
        - 5분마다 평균값 출력
        '''
        print(
            '환경 데이터 출력을 시작합니다. '
            f'종료하려면 \'{self.stop_key}\' 키를 누르세요.'
        )

        sample_count = 0

        while True:
            ds.set_env()
            self._copy_sensor_values()
            self._print_env_values()
            self._save_history()

            sample_count += 1

            if sample_count % 60 == 0:
                self._print_five_minute_average()

            for _ in range(5):
                if self._check_stop_key():
                    return
                time.sleep(1)


ds = DummySensor()
RunComputer = MissionComputer()

if __name__ == '__main__':
    RunComputer.get_sensor_data()