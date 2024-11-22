<template>
  <div class="home-container">
    <!-- 헤더 -->
    <header class="header">
      <h1>HOME</h1>
    </header>

    <!-- 카테고리 -->
    <section class="category-section">
      <h2>카테고리</h2>
      <div class="category-buttons">
        <!-- 지역 버튼들 -->
        <button @click="fetchArticles('전라북도')">전라북도</button>
        <button @click="fetchArticles('전라남도')">전라남도</button>
        <button @click="fetchArticles('충청남도')">충청남도</button>
        <button @click="fetchArticles('경상북도')">경상북도</button>
        <button @click="fetchArticles('경상남도')">경상남도</button>
        <button @click="fetchArticles('강원도')">강원도</button>
        <button @click="fetchArticles('부산시')">부산시</button>
        <button @click="fetchArticles('서울시')">서울시</button>
        <button @click="fetchArticles('인천시')">인천시</button>
        <button @click="fetchArticles('경기도')">경기도</button>
        <button @click="fetchArticles('대전시')">대전시</button>


  
      </div>
    </section>

    <!-- 뉴스 기사 리스트 -->
    <section class="news-articles">
      <h2>기사 목록</h2>
      <ul>
        <!-- 각 기사 항목 출력 -->
        <li v-for="article in articles" :key="article.id">
          <a :href="article.link" target="_blank">{{ article.title }}</a>
          <p>{{ article.description }}</p>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // 기사 데이터 배열
      articles: [],
    };
  },
  methods: {
    // 지역을 선택하여 API에서 데이터를 가져오는 메서드
    
    async fetchArticles(region) {
      console.log(region);
      
      try {
        // API 호출
        const response = await axios.get(`/news/region/${region}/`);
        // 가져온 데이터를 articles 배열에 저장
        this.articles = response.data;
      } catch (error) {
        console.error("기사 가져오기 실패:", error);
      }
    },
  },
};
</script>

<style scoped>
/* 추가적인 스타일링을 원하는 경우 여기에 작성 */
</style>
