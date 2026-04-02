import csv
import pickle


def process_mars_inventory(input_file, output_csv, output_bin):
    """
    화성 기지 재고를 정렬하여 CSV 및 이진 파일로 저장하고,
    이진 데이터의 원시 형태와 복구된 전체 내용을 출력함.
    """
    inventory_list = []

    try:
        # 1. CSV 파일 읽기
        with open(input_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file) #csv데이터를 한 줄씩 읽어서 리스트로 변환
            inventory_list = list(reader) # 전체 데이터를 한 번에 리스트로 저장

        if not inventory_list:
            print('데이터가 비어 있습니다.')
            return

        header = inventory_list[0] #첫번째 줄은 컬럼
        data = inventory_list[1:] #실제 데이터 저장

        # 2. 인화성(인덱스 4) 기준 내림차순 정렬
        data.sort(key=lambda x: float(x[4]), reverse=True) #인화성 값은 5번째 컬럼
        sorted_all = [header] + data

        # 3. 정렬된 내용을 이진 파일(.bin)로 저장
        with open(output_bin, mode='wb') as bin_file:
            pickle.dump(sorted_all, bin_file)
        print(f"✅ 이진 파일 저장 완료: '{output_bin}'")

        # 4. 저장된 이진 파일 다시 읽어서 전체 출력
        with open(output_bin, mode='rb') as bin_file:
            loaded_data = pickle.load(bin_file)
        
        print('\n--- [이진 파일에서 복구된 전체 내용] ---')
        for row in loaded_data:
            print(row)

        # 5. 인화성 0.7 이상 필터링 및 CSV 저장
        danger_list = [row for row in data if float(row[4]) >= 0.7] 
        with open(output_csv, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(danger_list)
        print(f"\n✅ 위험 물질 CSV 저장 완료: '{output_csv}'")

    except FileNotFoundError:
        print(f"❌ 오류: '{input_file}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f'❌ 오류 발생: {e}')
        dkfsldjfsldfj


if __name__ == '__main__':
    INPUT_FILE = 'Mars_Base_Inventory_List.csv'
    DANGER_CSV = 'Mars_Base_Inventory_danger.csv'
    DATA_BIN = 'Mars_Base_Inventory_List.bin'

    process_mars_inventory(INPUT_FILE, DANGER_CSV, DATA_BIN)