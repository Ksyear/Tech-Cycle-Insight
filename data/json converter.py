import csv
import json
from collections import defaultdict, Counter
import os

def process_data():
    """
    제공된 CSV 파일들을 읽어 JSON 형식으로 변환하는 함수.
    """
    file_path_tech_keywords = '(재)연구개발특구진흥재단_협약과제 키워드_20240826.csv'
    file_path_promising_tech = '(재)연구개발특구진흥재단_유망기술집_20230210.csv'
    file_path_rnd_expenditure = '(재)연구개발특구진흥재단_연구개발특구 연구개발비 현황_20211231.CSV'

    # 데이터를 저장할 딕셔너리
    tech_keywords = defaultdict(int)
    promising_techs = {}
    rnd_expenditure = {}

    try:
        # 협약과제 키워드 데이터 처리 (기술 동향 및 빈도 분석)
        # 'cp949' 인코딩으로 변경하여 한글 깨짐 오류를 해결
        with open(file_path_tech_keywords, 'r', encoding='cp949') as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row['키워드명'].strip()
                tech_keywords[keyword] += 1
    except FileNotFoundError:
        print(f"오류: {file_path_tech_keywords} 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return
    except UnicodeDecodeError:
        print(f"오류: {file_path_tech_keywords} 파일의 인코딩을 읽을 수 없습니다. 'utf-8' 또는 'cp949' 이외의 인코딩일 수 있습니다.")
        return

    try:
        # 유망기술집 데이터 처리 (기술 목록 및 상세 정보)
        with open(file_path_promising_tech, 'r', encoding='cp949') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tech_name = row['기술명'].strip()
                description = row['발명의 명칭'].strip()
                promising_techs[tech_name] = description
    except FileNotFoundError:
        print(f"오류: {file_path_promising_tech} 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return
    except UnicodeDecodeError:
        print(f"오류: {file_path_promising_tech} 파일의 인코딩을 읽을 수 없습니다. 'utf-8' 또는 'cp949' 이외의 인코딩일 수 있습니다.")
        return
        
    try:
        # 연구개발비 현황 데이터 처리 (기술의 성장 단계 판단)
        with open(file_path_rnd_expenditure, 'r', encoding='cp949') as f:
            reader = csv.DictReader(f)
            for row in reader:
                division = row['구분'].strip()
                # 쉼표(,) 제거 후 정수로 변환
                total_expenditure = int(row['총 연구개발비(백만원)'].replace(',', ''))
                rnd_expenditure[division] = total_expenditure
    except FileNotFoundError:
        print(f"오류: {file_path_rnd_expenditure} 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return
    except (UnicodeDecodeError, ValueError):
        print(f"오류: {file_path_rnd_expenditure} 파일을 처리하는 중 오류가 발생했습니다. 인코딩이나 데이터 형식을 확인해주세요.")
        return

    # 기술 수명 주기 및 포트폴리오 제안 데이터 생성
    tech_life_cycle = []
    portfolio_suggestions = {
        "high_risk": [],
        "medium_risk": [],
        "low_risk": []
    }

    # 모든 키워드를 기술 목록으로 사용
    all_techs = sorted(tech_keywords.keys())

    # 기술 단계 및 포트폴리오 분류 (가상 로직)
    # 실제 구현 시에는 더 복잡한 분석 로직이 필요
    # 모든 키워드를 활용하여 더 풍부한 데이터 생성
    for i, tech_name in enumerate(all_techs):
        stage = ""
        description = ""
        
        # 키워드 빈도에 따라 기술 단계 분류
        keyword_count = tech_keywords[tech_name]
        
        if keyword_count > 10:
            stage = "성숙"
            description = f"기술 성숙 단계로, 시장 점유율 확보를 위한 전략이 필요한 시점입니다. 관련 투자금액이 높고 시장 규모가 안정적입니다. ({tech_name})"
            portfolio_suggestions["low_risk"].append(tech_name)
        elif 5 < keyword_count <= 10:
            stage = "성장"
            description = f"기술 성장 단계로, 시장 확대가 빠르게 이루어지고 있습니다. 혁신적인 기술이 지속적으로 개발되고 있으며, 관련 투자도 활발합니다. ({tech_name})"
            portfolio_suggestions["medium_risk"].append(tech_name)
        else:
            stage = "초기"
            description = f"기술 초기 단계로, 아직 상용화되지 않았지만 잠재력이 큰 기술입니다. 관련 연구가 활발히 진행 중이며, 미래 가치가 높게 평가됩니다. ({tech_name})"
            portfolio_suggestions["high_risk"].append(tech_name)
        
        tech_life_cycle.append({
            "name": tech_name,
            "stage": stage,
            "description": description
        })

    final_json_data = {
        "tech_life_cycle": tech_life_cycle,
        "portfolio_suggestions": portfolio_suggestions
    }

    # JSON 파일로 저장
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_json_data, f, ensure_ascii=False, indent=2)
        print("data.json 파일이 성공적으로 생성되었습니다.")
    except IOError:
        print("오류: data.json 파일을 저장하는 데 실패했습니다.")

if __name__ == "__main__":
    process_data()
