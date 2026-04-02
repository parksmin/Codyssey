import random
import datetime


class DummySensor:
    """
    화성 기지의 환경 수치를 무작위로 생성하고 관리하며,
    조회 시 로그를 파일에 기록하는 더미 센서 클래스.
    """

    def __init__(self):
        """
        환경 변수를 저장할 사전(dict) 객체를 멤버로 초기화함.
        """
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        """
        각 환경 항목에 대해 지정된 범위 내의 랜덤 값을 생성하여 저장함.
        """
        self.env_values['mars_base_internal_temperature'] = \
            round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = \
            round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = \
            round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = \
            round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = \
            round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = \
            round(random.uniform(4, 7), 2)

    def get_env(self):
        """
        환경 데이터를 반환하고, 동시에 'mission_log.txt' 파일에 
        날짜와 환경 수치를 기록함 (보너스 과제 수행).
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 로그 메시지 포맷 구성
        log_msg = (
            f"[{now}] "
            f"내부온도: {self.env_values['mars_base_internal_temperature']}°C, "
            f"외부온도: {self.env_values['mars_base_external_temperature']}°C, "
            f"내부습도: {self.env_values['mars_base_internal_humidity']}%, "
            f"외부광량: {self.env_values['mars_base_external_illuminance']}W/m2, "
            f"CO2농도: {self.env_values['mars_base_internal_co2']}%, "
            f"산소농도: {self.env_values['mars_base_internal_oxygen']}%\n"
        )

        # 파일에 로그 추가 (Append 모드)
        try:
            with open('mission_log.txt', mode='a', encoding='utf-8') as f:
                f.write(log_msg)
        except Exception as e:
            print(f'로그 기록 중 오류 발생: {e}')

        return self.env_values


# --- 메인 실행부 ---
if __name__ == '__main__':
    # 1. 인스턴스 생성
    ds = DummySensor()

    # 2. 데이터 생성 호출
    ds.set_env()

    # 3. 데이터 조회 및 로그 기록 수행
    current_env = ds.get_env()

    # 4. 화면 출력 확인
    print('--- 화성 기지 미션 컴퓨터: 실시간 환경 리포트 ---')
    for key, value in current_env.items():
        # 가독성을 위해 키값 정리
        clean_name = key.replace('mars_base_', '').replace('_', ' ').title()
        print(f'{clean_name}: {value}')
    
    print("\n✅ 'mission_log.txt' 파일에 로그가 기록되었습니다.")