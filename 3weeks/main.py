import csv


def process_mars_inventory(input_file, output_file):
    """
    화성 기지 재고 목록을 읽어 인화성 지수가 높은 순으로 정렬하고,
    0.7 이상인 위험 물질을 별도 파일로 저장하는 함수.
    """
    inventory_list = []

    try:
        # 1. 파일 읽기 및 리스트 변환 (Standard Library 'csv' 사용)
        with open(input_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            inventory_list = list(reader)

        if not inventory_list:
            print('데이터가 비어 있습니다.')
            return

        header = inventory_list[0]
        data = inventory_list[1:]

        # 2. 인화성(Flammability, 인덱스 4) 높은 순으로 정렬
        # 대입문 = 앞뒤 공백 준수 및 람다 함수 활용
        data.sort(key=lambda x: float(x[4]), reverse=True)

        # 3. 인화성 지수가 0.7 이상인 목록 필터링
        danger_list = [row for row in data if float(row[4]) >= 0.7]

        # 4. 필터링된 목록 별도 출력
        print('\n--- [위험] 인화성 0.7 이상 물질 목록 ---')
        print(f'{header[0]:<20} | {header[4]}')
        print('-' * 35)
        for row in danger_list:
            print(f'{row[0]:<20} | {row[4]}')

        # 5. CSV 포맷으로 저장 (외부 패키지 없이 기본 csv.writer 사용)
        with open(output_file, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(danger_list)

        print(f"\n✅ 완료: '{output_file}' 파일이 생성되었습니다.")

    except FileNotFoundError:
        print(f"❌ 오류: '{input_file}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f'❌ 오류 발생: {e}')


if __name__ == '__main__':
    # 상수 정의 및 함수 실행
    INPUT_CSV = 'Mars_Base_Inventory_List.csv'
    OUTPUT_CSV = 'Mars_Base_Inventory_danger.csv'

    process_mars_inventory(INPUT_CSV, OUTPUT_CSV)