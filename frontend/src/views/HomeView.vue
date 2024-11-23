<template>
  <div class="home-view">
    <h1>뉴스 기사 목록</h1>
    <div>
      <h2>지역 선택:</h2>
      <div class="region-buttons">
        <!-- 모든 지역 보기 버튼 -->
        <button
          v-for="region in regions"
          :key="region"
          @click="setRegion(region)"
          :class="{ active: selectedRegion === region }"
        >
          {{ region }}
        </button>
        <button
          @click="setRegion('')"
          :class="{ active: selectedRegion === '' }"
        >
          모든 지역
        </button>
      </div>
    </div>

    <div v-if="loading">뉴스 데이터를 가져오는 중...</div>

    <div v-else-if="articles.length === 0">
      선택한 지역에 대한 뉴스 정보가 없습니다.
    </div>

    <div v-else>
      <ul>
        <li v-for="article in articles" :key="article.id">
          <h3>{{ article.title }}</h3>
          <p><strong>발행일:</strong> {{ article.pub_date }}</p>
          <p><strong>내용:</strong> {{ article.description }}</p>
          <p>
            <strong>원문 링크:</strong>
            <a :href="article.originallink" target="_blank">기사 읽기</a>
          </p>
        </li>
      </ul>
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
      articles: [], // 뉴스 데이터
      loading: false, // 로딩 상태
    };
  },
  methods: {
    // 선택된 지역 설정 및 뉴스 데이터 가져오기
    setRegion(region) {
      this.selectedRegion = region;
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
.home-view {
  padding: 20px;
}

.region-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
}

button.active {
  background-color: #007bff;
  color: white;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 15px 0;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
</style>
