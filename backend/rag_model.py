import os
import sys
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from document_store import DocumentStore
from dotenv import load_dotenv
from datetime import datetime
import django

# Django settings 모듈 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Django 설정을 로드
django.setup()

# 환경 변수 로드
load_dotenv()

class StreamHandler(BaseCallbackHandler):
    """스트리밍 중간 응답을 처리하는 핸들러"""
    def __init__(self, container=None):
        # container가 None이 아닌 경우에만 empty 메서드를 호출합니다.
        if container is not None:
            self.message_placeholder = container.empty()
        else:
            self.message_placeholder = None
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        if self.message_placeholder is not None:
            self.message_placeholder.markdown(self.text)

class RAGChatbot:
    """
    RAG 기반 챗봇 클래스
    """
    def __init__(self, collection_name="festival_news"):
        # NewsDocumentStore 초기화
        self.doc_store = DocumentStore.from_existing(collection_name)

        # LLM 초기화
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7,
            streaming=True
        )
    
    def search_documents(self, query: str, k: int = 3):
        """
        문서 검색 함수
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 개수
        
        Returns:
            관련 문서 리스트
        """
        try:
            return self.doc_store.similarity_search(query, k=k)
        except Exception as e:
            raise RuntimeError(f"문서 검색 중 오류 발생: {str(e)}")
    
    def generate_answer(self, query: str, relevant_docs: list, stream_handler=None):
        """
        LLM을 사용해 답변 생성
        
        Args:
            query: 사용자 질문
            relevant_docs: 검색된 관련 문서 리스트
            stream_handler: 스트리밍 핸들러
        
        Returns:
            생성된 답변 문자열
        """
        if stream_handler is None:
            stream_handler = StreamHandler(container=None)  # 기본 스트림 핸들러 설정

        # 시스템 프롬프트 구성
        system_prompt = """당신은 사용자의 질문에 대해 친절하고 전문적으로 답변하는 축제 가이드 AI 어시스턴트입니다.
        제공된 문서 정보를 바탕으로 답변하되, 문서 내용을 벗어나지 않도록 주의하세요.
        답변은 한국어로 작성하며, 이해하기 쉽게 설명하세요.
        축제 정보를 제공하는 것이 목적입니다.
        축제 기간이 오늘 날짜 기준 지난 축제의 정보는 제공하지 마세요."""
        
        # 관련 문서 정보를 컨텍스트로 추가
        context = "관련 문서 정보:\n"
        for i, doc in enumerate(relevant_docs, 1):
            context += f"{i}. {doc['content'][:300]}...\n"  # 문서 일부만 포함
        
        # 메시지 구성
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"{context}\n\n질문: {query}")
        ]
        
        # GPT 모델을 통한 답변 생성
        try:
            response = self.llm(messages, callbacks=[stream_handler])
            return response.content
        except Exception as e:
            raise RuntimeError(f"답변 생성 중 오류 발생: {str(e)}")

# 사용 예시
if __name__ == "__main__":
    # RAG 챗봇 인스턴스 초기화
    chatbot = RAGChatbot(collection_name="festival_news")
    
    # 예제 쿼리
    query = "20424년 11월 25일에 하고 있는 축제 추천해줘"
    
    # 문서 검색
    print("문서 검색 중...")
    results = chatbot.search_documents(query)
    
    # print(results)
    # 검색 결과 출력
    for i, result in enumerate(results, 1):
        print(f"\n=== 문서 {i} ===")
        print(f"제목: {result['metadata'].get('title', '제목 없음')}")
        print(f"내용: {result['content'][:200]}...")
        print(f"유사도: {result['similarity']:.2%}")
    
    # GPT를 통한 답변 생성
    print("\n답변 생성 중...")
    stream_handler = StreamHandler(container=None)  # 출력용 핸들러
    answer = chatbot.generate_answer(query, results, stream_handler)
    
    print("\n=== 생성된 답변 ===")
    print(answer)