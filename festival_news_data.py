import os
import urllib.request
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv 

# .env 파일에서 환경 변수 로드
load_dotenv()

# 네이버 API 인증 정보
client_id = os.getenv("CLIENT_ID")  # 발급받은 Client ID 입력
client_secret = os.getenv("CLIENT_SECRET")  # 발급받은 Client Secret 입력


# 여러 JSON 파일에서 축제 이름 불러오기
def load_festival_names_from_multiple_files(directory):
    festival_names = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                festival_names.extend([festival['Title'] for festival in data])
    return festival_names


# 네이버 뉴스 API 요청
def search_news(query):
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&display=100"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    if response.getcode() == 200:
        return json.loads(response.read().decode('utf-8'))
    else:
        print(f"Error Code: {response.getcode()}")
        return None


# 최근 12개월 이내의 기사만 필터링하고 중복 제거
def filter_recent_articles(articles, months=12):
    cutoff_date = (datetime.now() - timedelta(days=30 * months)).replace(tzinfo=timezone.utc)
    seen_links = set()  # 중복 확인을 위한 집합
    recent_articles = []
    
    for article in articles:
        try:
            pub_date = datetime.strptime(article['pubDate'], "%a, %d %b %Y %H:%M:%S %z")
            link = article.get('link')  # 기사 고유 링크
            
            if pub_date > cutoff_date and link not in seen_links:
                seen_links.add(link)  # 처리한 링크 기록
                recent_articles.append(article)
        except (ValueError, KeyError):
            print(f"Invalid article data skipped: {article}")
    
    return recent_articles


# 중복된 기사 제거 및 통합
def remove_duplicate_articles(all_results):
    seen_links = set()  # 전체 중복 확인을 위한 집합
    unique_results = []

    for result in all_results:
        for festival, articles in result.items():
            unique_articles = []
            for article in articles:
                link = article.get('link')
                if link not in seen_links:
                    seen_links.add(link)
                    unique_articles.append(article)
            unique_results.append({festival: unique_articles})

    return unique_results


# 결과 저장
def save_results(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


# 메인 함수 
def main():
    # JSON 파일들이 저장된 디렉토리 경로
    directory = "../data/festival_info/"
    output_file = "../data/festival_news/festival_news_data.json"
    
    # 모든 축제 이름 불러오기
    festival_names = load_festival_names_from_multiple_files(directory)
    all_results = []

    for name in festival_names:
        print(f"Searching news for: {name}")
        response = search_news(name)
        if response and 'items' in response:
            recent_articles = filter_recent_articles(response['items'])
            all_results.append({name: recent_articles})
        else:
            print(f"No articles found for {name}")

    # 중복 제거 및 통합
    unique_results = remove_duplicate_articles(all_results)

    # 결과 저장
    save_results(unique_results, output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()