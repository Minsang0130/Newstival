<template>
  <div class="home-container">
    <!-- 헤더 -->
    <header class="header">
      <h1>HOME</h1>
      <nav class="nav-links">
        <a href="/signup">회원가입</a> | 
        <a href="/login">로그인</a> | 
        <a href="/board">게시판</a>
      </nav>
    </header>

    <!-- 카테고리 -->
    <section class="category-section">
      <h2>카테고리</h2>
      <div class="category-buttons">
        <button class="category-btn">지역 1</button>
        <button class="category-btn">지역 2</button>
        <button class="category-btn">지역 3</button>
        <button class="category-btn">지역 4</button>
        <button class="category-btn">지역 5</button>
        <button class="category-btn">지역 6</button>
        <button class="category-btn">지역 7</button>
        <button class="category-btn">지역 8</button>
      </div>
    </section>

    <!-- 기사 리스트 -->
    <section class="news-section">
      <h2>기사</h2>
      <div class="news-list">
        <div class="news-item">기사 1</div>
        <div class="news-item">기사 2</div>
        <div class="news-item">기사 3</div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 전체 컨테이너 */
.home-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
}

/* 헤더 */
.header {
  text-align: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.nav-links {
  font-size: 16px;
}

.nav-links a {
  text-decoration: none;
  color: #5e35b1;
  font-weight: bold;
  margin: 0 10px;
}

.nav-links a:hover {
  color: #311b92;
}

/* 카테고리 섹션 */
.category-section {
  margin-bottom: 30px;
}

.category-section h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category-btn {
  padding: 10px 20px;
  background-color: #f48fb1;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.category-btn:hover {
  background-color: #ec407a;
}

/* 기사 섹션 */
.news-section {
  margin-top: 20px;
}

.news-section h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.news-item {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  font-size: 18px;
}
</style>
