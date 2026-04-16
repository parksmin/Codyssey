import json
import os
import platform
import random
import subprocess
import time


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
    더미 센서의 값을 받아 화성 기지의 환경 정보와
    시스템 정보를 출력하는 미션 컴퓨터 클래스
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
        self.setting_file = 'setting.txt'
        self._create_setting_file()

    def _create_setting_file(self):
        '''
        setting.txt 파일이 없으면 기본 항목으로 생성한다.
        '''
        if os.path.exists(self.setting_file):
            return

        default_items = [
            'mars_base_internal_temperature',
            'mars_base_external_temperature',
            'mars_base_internal_humidity',
            'mars_base_external_illuminance',
            'mars_base_internal_co2',
            'mars_base_internal_oxygen',
            'operating_system',
            'operating_system_version',
            'cpu_type',
            'cpu_core_count',
            'memory_size',
            'cpu_realtime_usage',
            'memory_realtime_usage',
        ]

        try:
            with open(self.setting_file, mode='w', encoding='utf-8') as file:
                for item in default_items:
                    file.write(f'{item}\n')
        except OSError:
            print('setting.txt 파일 생성 중 오류가 발생했습니다.')

    def _load_setting_items(self):
        '''
        setting.txt 파일에서 출력할 항목 목록을 읽어온다.
        파일이 없거나 비어 있으면 None을 반환한다.
        '''
        try:
            with open(self.setting_file, mode='r', encoding='utf-8') as file:
                items = []

                for line in file:
                    item = line.strip()
                    if item:
                        items.append(item)

                if items:
                    return items
        except FileNotFoundError:
            return None
        except OSError:
            return None

        return None

    def _filter_output_items(self, data):
        '''
        setting.txt에 지정된 항목만 골라서 반환한다.
        setting.txt가 없거나 비어 있으면 전체 데이터를 반환한다.
        '''
        setting_items = self._load_setting_items()

        if setting_items is None:
            return data

        filtered_data = {}

        for key in setting_items:
            if key in data:
                filtered_data[key] = data[key]

        if filtered_data:
            return filtered_data

        return data

    def get_sensor_data(self):
        '''
        센서 값을 가져와 env_values에 저장하고 JSON 형식으로 출력한다.
        '''
        ds.set_env()
        self.env_values = ds.get_env()

        output_data = self._filter_output_items(self.env_values)

        print('=== 화성 기지 환경 정보 ===')
        print(json.dumps(output_data, indent=4, ensure_ascii=False))
        print()

        return output_data

    def get_mission_computer_info(self):
        '''
        미션 컴퓨터의 시스템 정보를 가져와 JSON 형식으로 출력한다.
        '''
        try:
            operating_system = platform.system()
        except Exception:
            operating_system = '확인 불가'

        try:
            operating_system_version = platform.version()
        except Exception:
            operating_system_version = '확인 불가'

        try:
            cpu_type = platform.processor()
            if not cpu_type:
                cpu_type = '확인 불가'
        except Exception:
            cpu_type = '확인 불가'

        try:
            cpu_core_count = os.cpu_count()
            if cpu_core_count is None:
                cpu_core_count = '확인 불가'
        except Exception:
            cpu_core_count = '확인 불가'

        try:
            memory_size = self._get_memory_size()
        except Exception:
            memory_size = '확인 불가'

        info_data = {
            'operating_system': operating_system,
            'operating_system_version': operating_system_version,
            'cpu_type': cpu_type,
            'cpu_core_count': cpu_core_count,
            'memory_size': memory_size,
        }

        output_data = self._filter_output_items(info_data)

        print('=== 미션 컴퓨터 시스템 정보 ===')
        print(json.dumps(output_data, indent=4, ensure_ascii=False))
        print()

        return output_data

    def _get_memory_size(self):
        '''
        전체 메모리 크기를 문자열 형태로 반환한다.
        '''
        system_name = platform.system()

        if system_name == 'Windows':
            result = subprocess.run(
                [
                    'wmic',
                    'ComputerSystem',
                    'get',
                    'TotalPhysicalMemory',
                    '/value',
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():
                if 'TotalPhysicalMemory=' in line:
                    memory_bytes = int(line.split('=')[1].strip())
                    memory_gb = round(memory_bytes / (1024 ** 3), 2)
                    return f'{memory_gb} GB'

        elif system_name in ('Linux', 'Darwin'):
            if hasattr(os, 'sysconf'):
                page_size = os.sysconf('SC_PAGE_SIZE')
                page_count = os.sysconf('SC_PHYS_PAGES')
                memory_bytes = page_size * page_count
                memory_gb = round(memory_bytes / (1024 ** 3), 2)
                return f'{memory_gb} GB'

        return '확인 불가'

    def get_mission_computer_load(self):
        '''
        미션 컴퓨터의 CPU 및 메모리 실시간 사용량을
        JSON 형식으로 출력한다.
        '''
        try:
            cpu_usage = self._get_cpu_usage()
        except Exception:
            cpu_usage = '확인 불가'

        try:
            memory_usage = self._get_memory_usage()
        except Exception:
            memory_usage = '확인 불가'

        load_data = {
            'cpu_realtime_usage': cpu_usage,
            'memory_realtime_usage': memory_usage,
        }

        output_data = self._filter_output_items(load_data)

        print('=== 미션 컴퓨터 부하 정보 ===')
        print(json.dumps(output_data, indent=4, ensure_ascii=False))
        print()

        return output_data

    def _get_cpu_usage(self):
        '''
        운영체제에 따라 CPU 실시간 사용량을 문자열 형태로 반환한다.
        '''
        system_name = platform.system()

        if system_name == 'Windows':
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'loadpercentage', '/value'],
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():
                if 'LoadPercentage=' in line:
                    value = line.split('=')[1].strip()
                    return f'{value}%'

        elif system_name == 'Linux':
            first = self._read_linux_cpu_stat()
            time.sleep(1)
            second = self._read_linux_cpu_stat()

            idle_time = second['idle'] - first['idle']
            total_time = second['total'] - first['total']

            if total_time > 0:
                usage = round((1 - idle_time / total_time) * 100, 2)
                return f'{usage}%'

        return '확인 불가'

    def _read_linux_cpu_stat(self):
        '''
        Linux에서 /proc/stat 파일을 읽어 CPU 사용량 계산용 값을 반환한다.
        '''
        with open('/proc/stat', mode='r', encoding='utf-8') as file:
            first_line = file.readline()

        values = first_line.split()
        numbers = [int(value) for value in values[1:]]

        idle = numbers[3]
        total = sum(numbers)

        return {
            'idle': idle,
            'total': total,
        }

    def _get_memory_usage(self):
        '''
        운영체제에 따라 메모리 실시간 사용량을 문자열 형태로 반환한다.
        '''
        system_name = platform.system()

        if system_name == 'Windows':
            result = subprocess.run(
                [
                    'wmic',
                    'OS',
                    'get',
                    'FreePhysicalMemory,TotalVisibleMemorySize',
                    '/value',
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            free_memory = None
            total_memory = None

            for line in result.stdout.splitlines():
                if 'FreePhysicalMemory=' in line:
                    free_memory = int(line.split('=')[1].strip())
                elif 'TotalVisibleMemorySize=' in line:
                    total_memory = int(line.split('=')[1].strip())

            if free_memory is not None and total_memory is not None:
                used_memory = total_memory - free_memory
                used_percent = round((used_memory / total_memory) * 100, 2)
                return f'{used_percent}%'

        elif system_name == 'Linux':
            memory_info = {}

            with open('/proc/meminfo', mode='r', encoding='utf-8') as file:
                for line in file:
                    key, value = line.split(':')
                    memory_info[key] = int(value.strip().split()[0])

            total_memory = memory_info.get('MemTotal')
            available_memory = memory_info.get('MemAvailable')

            if total_memory and available_memory is not None:
                used_memory = total_memory - available_memory
                used_percent = round((used_memory / total_memory) * 100, 2)
                return f'{used_percent}%'

        return '확인 불가'


ds = DummySensor()
runComputer = MissionComputer()

if __name__ == '__main__':
    runComputer.get_sensor_data()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()