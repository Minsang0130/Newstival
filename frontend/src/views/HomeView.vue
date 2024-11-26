<template>
  <div class="home-view">
    <!-- 헤더 -->
    <header class="header">
      <h1>🌸 지역별 뉴스 & 축제 소식 🌸</h1>
      <p>선택한 지역의 뉴스와 소식을 확인해보세요!</p>
    </header>

    <!-- 지역 선택 -->
    <section class="region-section">
      <h2>지역 선택</h2>
      <div class="region-buttons">
        <!-- 모든 지역 버튼 -->
        <button
          @click="setRegion('')"
          :class="{ active: selectedRegion === '' }"
          class="all-region-button"
        >
          모든 지역
        </button>

        <!-- 지역별 버튼 -->
        <button
          v-for="region in regions"
          :key="region"
          @click="setRegion(region)"
          :class="{ active: selectedRegion === region }"
        >
          {{ region }}
        </button>
      </div>
    </section>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading">
      <p>🎡 뉴스를 불러오는 중입니다... 잠시만 기다려주세요! 🎡</p>
    </div>

    <!-- 데이터 없음 -->
    <div v-else-if="paginatedArticles.length === 0" class="no-data">
      <p>선택한 지역에 해당하는 뉴스 기사가 없습니다. 다른 지역을 선택해보세요!</p>
    </div>

    <!-- 뉴스 기사 목록 -->
    <section v-else class="news-section">
      <ul>
        <li v-for="article in paginatedArticles" :key="article.id" class="news-card">
          <h3>{{ article.title }}</h3>
          <p><strong>발행일:</strong> {{ article.pub_date }}</p>
          <p><strong>내용:</strong> {{ article.description }}</p>
          <p>
            <strong>원문 링크:</strong>
            <a :href="article.originallink" target="_blank">기사 읽기</a>
          </p>
        </li>
      </ul>

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--">◀ 이전</button>
        <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++">다음 ▶</button>
      </div>
    </section>
    
<!-- 챗봇 열기/닫기 버튼 -->
<div class="chatbot-toggle" @click="toggleChat">
      <span v-if="!isChatOpen">🤖</span>
      <span v-else>❌</span>
    </div>

    <!-- 챗봇 -->
    <div v-if="isChatOpen" class="chatbot">
      <!-- 새로운 상단 박스 영역 -->
      <div class="chatbot-header">
        <span class="chatbot-name">Festival Chatbot 🤖</span>
        <button class="close-chat" @click="closeChat">닫기</button>
      </div>

      <div id="chat-container" class="chat-messages">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="message.isUser ? 'user-message' : 'bot-message'"
        >
          <span v-if="message.isLoading">⏳ 메시지 처리 중...</span>
          <span v-else>{{ message.text }}</span>
        </div>
      </div>

      <!-- 사용자 입력 -->
      <div class="chat-input">
        <input
          v-model="userInput"
          placeholder="질문을 입력하세요..."
          @keyup.enter="sendMessage"
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="loading">전송</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      regions: [
        "전라북도",
        "전라남도",
        "충청남도",
        "경상북도",
        "경상남도",
        "강원도",
        "부산시",
        "서울시",
        "인천시",
        "경기도",
        "대전시",
      ], // 지역 목록
      selectedRegion: "", // 선택된 지역 (기본값: 모든 지역)
      articles: [], // 모든 뉴스 데이터
      loading: false, // 로딩 상태
      currentPage: 1, // 현재 페이지
      articlesPerPage: 5, // 페이지당 기사 수
      userInput: "", // 사용자 입력 내용
      messages: [], // 채팅 메시지 배열
      loading: false, // 로딩 상태
      isChatOpen: false, // 챗봇 열기/닫기 상태
    };
  },
  computed: {
    // 현재 페이지에 해당하는 기사 목록
    paginatedArticles() {
      const start = (this.currentPage - 1) * this.articlesPerPage;
      const end = start + this.articlesPerPage;
      return this.articles.slice(start, end);
    },
    // 총 페이지 수
    totalPages() {
      return Math.ceil(this.articles.length / this.articlesPerPage);
    },
  },
  methods: {
    // 선택된 지역 설정 및 뉴스 데이터 가져오기
    setRegion(region) {
      this.selectedRegion = region;
      this.currentPage = 1; // 페이지를 1로 초기화
      this.fetchArticles();
    },
    async fetchArticles() {
      this.loading = true;

      try {
        const url = this.selectedRegion
          ? `/news/region/${encodeURIComponent(this.selectedRegion)}/` // 특정 지역 뉴스
          : `/news/`; // 모든 지역 뉴스

        const response = await axios.get(url); // Axios 요청
        this.articles = response.data; // 데이터 저장
      } catch (error) {
        console.error("Error fetching articles:", error);
        this.articles = []; // 요청 실패 시 빈 데이터
      } finally {
        this.loading = false;
      }
    },
    async sendMessage() {
      const input = this.userInput.trim();
      if (!input) return;

      this.messages.push({ text: input, isUser: true, isLoading: false });
      this.userInput = "";

      const botMessageIndex = this.messages.length;
      this.messages.push({ text: "처리 중...", isUser: false, isLoading: true });

      try {
        const response = await axios.post("http://127.0.0.1:8000/dashboard/chatbot/", {
          question: input,
        });

        this.messages[botMessageIndex].text = response.data.answer || "응답을 받을 수 없습니다.";
      } catch (error) {
        console.error("Chatbot API 호출 에러:", error);
        this.messages[botMessageIndex].text = "오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
      } finally {
        this.messages[botMessageIndex].isLoading = false;
        this.scrollToBottom(); // 최신 메시지로 자동 스크롤
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$el.querySelector("#chat-container");
        if (container) container.scrollTop = container.scrollHeight;
      });
    },
    toggleChat() {
      this.isChatOpen = !this.isChatOpen;
    },
    closeChat() {
      this.isChatOpen = false;
    },
  },
  watch: {
    messages() {
      this.scrollToBottom();
    }
  },
  mounted() {
    // 페이지 로드 시 모든 뉴스 데이터 가져오기
    this.fetchArticles();
  },
};
</script>

<style scoped>
/* 전체 레이아웃 */
.home-view {
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
  background: linear-gradient(to bottom, #fef6f8, #fff);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 헤더 */
.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.6rem;
  font-weight: bold;
  color: #e91e63;
}

.header p {
  font-size: 1rem;
  color: #666;
}

/* 지역 버튼 */
.region-section {
  margin-bottom: 40px;
  text-align: center;
}

.region-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* 가운데 정렬 */
  gap: 12px;
}

button {
  background-color: #ffebee;
  color: #e91e63;
  border: 2px solid #f8bbd0;
  border-radius: 20px;
  padding: 10px 15px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button.active {
  background-color: #e91e63;
  color: white;
  border-color: #ad1457;
}

button:hover {
  background-color: #ad1457;
  color: white;
  transform: translateY(-3px) scale(1.2); /* 확대 효과 추가 */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* 그림자 효과 추가 */
}

/* "모든 지역" 버튼 */
.all-region-button {
  font-weight: bold;
}

/* 로딩 상태 */
.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #757575;
}

/* 데이터 없음 */
.no-data {
  text-align: center;
  font-size: 1.2rem;
  color: #999;
}

/* 뉴스 카드 */
.news-section ul {
  list-style: none;
  padding: 0;
}

.news-card {
  background: white;
  border: 2px solid #fce4ec;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.news-card h3 {
  font-size: 1.5rem;
  color: #e91e63;
}

.news-card p {
  font-size: 1rem;
  color: #555;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.pagination button {
  background-color: #e91e63;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button:hover {
  background-color: #c2185b;
}

.pagination button:disabled {
  background-color: #f8bbd0;
  cursor: not-allowed;
}
/* 챗봇 열기/닫기 버튼 */
.chatbot-toggle {
  position: fixed;
  right: 20px;
  bottom: 100px;
  width: 50px;
  height: 50px;
  background-color: #e91e63;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.5rem;
}

/* 챗봇 */
.chatbot {
  position: fixed;
  right: 20px;
  bottom: 20px;
  width: 300px;
  height: 400px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
}

.user-message {
  text-align: right;
  background-color: #e0f7fa;
  padding: 8px;
  border-radius: 10px;
  margin-bottom: 5px;
}

.bot-message {
  text-align: left;
  background-color: #fce4ec;
  padding: 8px;
  border-radius: 10px;
  margin-bottom: 5px;
}

.chat-input {
  display: flex;
  border-top: 1px solid #ccc;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: none;
  outline: none;
  border-radius: 0 0 0 8px;
}

.chat-input button {
  padding: 10px;
  border: none;
  cursor: pointer;
  background-color: #0288d1;
  color: white;
  border-radius: 0 0 8px 0;
}

.chat-input input:disabled,
.chat-input button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

/* 챗봇 상단 박스 영역 스타일 */
.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  background-color: #fce4ec;
  border-bottom: 1px solid #ccc;
}

.chatbot-name {
  font-size: 1rem;
  font-weight: bold;
  color: #e91e63;
}

.close-chat {
  background-color: transparent;
  color: #f44336;
  border: none;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
}
</style>


