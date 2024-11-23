<template>
  <div class="home-view">
    <h1>뉴스 기사 목록</h1>
    <div>
      <label for="region-select">지역 선택:</label>
      <select id="region-select" v-model="selectedRegion" @change="fetchArticles">
        <option value="">모든 지역</option> <!-- 기본값으로 "모든 지역" 추가 -->
        <option v-for="region in regions" :key="region" :value="region">
          {{ region }}
        </option>
      </select>
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
      selectedRegion: "", // 선택한 지역 (기본값은 "모든 지역")
      articles: [], // 뉴스 데이터
      loading: false, // 로딩 상태
    };
  },
  methods: {
    async fetchArticles() {
      this.loading = true;

      try {
        // 지역 선택 여부에 따라 API 요청 URL 설정
        const url = this.selectedRegion
          ? `/news/region/${encodeURIComponent(this.selectedRegion)}/`
          : `/news/`; // 모든 지역의 뉴스 데이터 가져오기

        const response = await axios.get(url);
        this.articles = response.data; // 데이터 저장
      } catch (error) {
        console.error("Error fetching articles:", error);
        this.articles = []; // 데이터 초기화
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    // 페이지 로드 시 모든 지역의 뉴스 데이터를 기본적으로 가져옴
    this.fetchArticles();
  },
};
</script>

<style scoped>
.home-view {
  padding: 20px;
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
