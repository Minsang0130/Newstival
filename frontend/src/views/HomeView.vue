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
</style>
