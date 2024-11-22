import requests
from bs4 import BeautifulSoup
import json
import os

# 기본 URL
base_url = "https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pMenuCD=&pCurrentPage={page}&pSearchType=01&pSearchWord=&pSeq=&pSido=&pOrder=01up&pPeriod=pTMonth&fromDt=2024.11.20.&toDt=2025.02.20."

# 세부 페이지 Base URL
detail_base_url = "https://www.mcst.go.kr/kor/s_culture/festival/"

# 결과 저장용 리스트
festival_data = []

# 1페이지부터 12페이지까지 반복
for page in range(1, 13):  # 테스트를 위해 1페이지로 제한
    url = base_url.format(page=page)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 상세보기 href 추출
        for a_tag in soup.find_all('a', class_='go'):
            href = a_tag.get('href')
            if href:
                # 세부 URL 구성
                detail_url = detail_base_url + href
                
                # 세부 페이지 크롤링
                detail_response = requests.get(detail_url)
                if detail_response.status_code == 200:
                    detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                    
                    # 데이터 추출
                    try:
                        title = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > div.view_title').get_text(strip=True)
                    except AttributeError:
                        title = None
                        
                    try:
                        region = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > dl > dd:nth-child(2)').get_text(strip=True)
                    except AttributeError:
                        region = None
                        
                    # Main Region 추출
                    if region:
                        main_region = region.split()[0]
                    else:
                        main_region = None
                        
                    try:
                        period = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > dl > dd:nth-child(4)').get_text(strip=True)
                    except AttributeError:
                        period = None
                        
                    try:
                        nature = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > dl > dd:nth-child(6)').get_text(strip=True)
                    except AttributeError:
                        nature = None
                        
                    try:
                        fee = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > dl > dd:nth-child(12)').get_text(strip=True)
                    except AttributeError:
                        fee = None
                        
                    try:
                        info = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > div.view_con').get_text(strip=True)
                    except AttributeError:
                        info = None

                    try:
                        related_website = detail_soup.select_one('#content > div.contentWrap > div.viewWarp > dl > dd:nth-child(8) > a').get_text(strip=True)
                    except AttributeError:
                        related_website = None
                        
                    # Title이 None이 아니면 저장
                    if title:
                        festival_data.append({
                            'Title': title,
                            'Region': region,
                            'Main Region': main_region,
                            'Period': period,
                            'Nature': nature,
                            'Fee': fee,
                            'Info': info,
                            'Related Website': related_website,
                            'URL': detail_url
                        })

os.makedirs('data/festival_info', exist_ok=True)
# JSON 파일 저장
with open('data/festival_info/festival_details.json', 'w', encoding='utf-8') as json_file:
    json.dump(festival_data, json_file, ensure_ascii=False, indent=4)

# JSON 파일 출력 확인
print(json.dumps(festival_data, ensure_ascii=False, indent=4))
