import os

def analyze_mission_logs(file_path):
    # 제약조건: 문자열은 ''를 기본 사용
    target_keywords = ['unstable', 'explosion']
    output_file = 'problem_logs.txt'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 첫 번째 줄(헤더)을 제외하고 한 줄씩 리스트로 읽어옵니다.
            lines = file.readlines()
            header = lines[0]
            data_lines = lines[1:]

        # 1. 시간의 역순으로 정렬 (리스트 뒤집기)
        # log는 이미 시간순이므로 단순히 역순(reversed)으로 만들면 됩니다.
        reversed_logs = data_lines[::-1]

        print('--- 로그 출력 (시간 역순) ---')
        for log in reversed_logs:
            print(log.strip())

        # 2. 문제가 되는 부분(Keywords)만 추출하여 파일 저장
        problem_logs = []
        for log in data_lines:
            # 소문자로 변환하여 키워드가 포함되어 있는지 확인
            if any(key in log.lower() for key in target_keywords):
                problem_logs.append(log)

        if problem_logs:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header)  # 헤더 포함
                f.writelines(problem_logs)
            print(f'\n✅ 문제 로그 추출 완료: {output_file} 저장됨.')
        
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f'알 수 없는 예외 발생: {e}')

# 실행
analyze_mission_logs('mission_computer_main.log')