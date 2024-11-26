from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from datetime import datetime
from django.db.utils import OperationalError
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.conf import settings

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Now Django should be configured, and we can import Django models


class DocumentStore:
    """
    뉴스 기사를 위한 문서 저장 및 검색 시스템.
    Django ORM을 사용하여 데이터베이스 접근.
    """

    def __init__(self, collection_name: str = "festival_news"):
        # 환경 변수 로드
        load_dotenv()

        # 임베딩 모델 초기화
        self.embeddings = OpenAIEmbeddings()
        self.collection_name = collection_name

        # from festivals_news.models import FestivalNews

    def process_news_article(self, article: Dict) -> Dict:
        """
        뉴스 기사 데이터를 처리하여 문서와 메타데이터로 변환합니다.
        """
        content = f"{article['title']}\n\n{article['description']}"
        metadata = {
            'title': article['title'],
            'date_published': article.get('pub_date', ''),
            'url': article.get('originallink', ''),
        }
        return {
            'content': content,
            'metadata': metadata
        }

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        코사인 유사도를 사용해 유사한 문서를 검색합니다.
        """
        from festivals_news.models import FestivalNews
        try:
            # 데이터베이스에서 모든 문서 가져오기
            articles = FestivalNews.objects.all()

            # 뉴스 기사 내용을 벡터화
            docs = [
                f"{article.title}\n\n{article.description}" 
                for article in articles
            ]
            doc_vectors = self.embeddings.embed_documents(docs)

            # 쿼리를 벡터화
            query_vector = self.embeddings.embed_query(query)

            # 코사인 유사도 계산
            similarities = cosine_similarity([query_vector], doc_vectors).flatten()

            # 상위 k개 결과 정렬
            top_k_indices = np.argsort(similarities)[-k:][::-1]

            # 결과 생성
            results = []
            for idx in top_k_indices:
                # Convert idx to integer
                idx = int(idx)
                article = articles[idx]
                results.append({
                    'id': article.id,
                    'title': article.title,
                    'content': article.description,
                    'similarity': similarities[idx],
                    'metadata': {
                        'title': article.title,
                        # Add other metadata here if needed
                    }
                })

            return results
        except Exception as e:
            print(f"Error during similarity search: {e}")
            return []

    @classmethod
    def from_existing(cls, collection_name: str):
        """
        기존 컬렉션에서 초기화.
        """
        from festivals_news.models import FestivalNews
        instance = cls(collection_name)
        return instance

    def delete_collection(self):
        """
        컬렉션 삭제.
        """
        from festivals_news.models import FestivalNews
        try:
            FestivalNews.objects.filter(festival_name=self.collection_name).delete()
            print(f"Collection '{self.collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting collection: {e}")