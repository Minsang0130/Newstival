<template>
  <div class="event-schedule">
    <!-- 헤더 -->
    <header class="header">
      <h1>🎤 지역별 행사 일정 🎵</h1>
      <p>원하는 지역을 선택하고 다채로운 행사를 확인해보세요!</p>
    </header>

    <!-- 지역 선택 -->
    <section class="region-section">
      <label for="region-select" class="region-label">🌍 지역 선택</label>
      <select
        id="region-select"
        v-model="selectedRegion"
        @change="fetchEvents"
        class="region-select"
      >
        <option value="">모든 지역</option>
        <option v-for="region in regions" :key="region" :value="region">
          {{ region }}
        </option>
      </select>
    </section>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading">
      <p>🔄 데이터를 불러오는 중입니다. 잠시만 기다려주세요! 🔄</p>
    </div>

    <!-- 데이터 없음 -->
    <div v-else-if="paginatedEvents.length === 0" class="no-data">
      <p>😔 선택한 지역에 해당하는 행사가 없습니다. 다른 지역을 선택해주세요!</p>
    </div>

    <!-- 행사 목록 -->
    <section v-else class="events-section">
      <ul>
        <li v-for="event in paginatedEvents" :key="event.id" class="event-card">
          <h3>{{ event.title }}</h3>
          <p><strong>📅 기간:</strong> {{ event.period }}</p>
          <p><strong>📍 지역:</strong> {{ event.region }}</p>
          <p><strong>📖 정보:</strong> {{ event.info }}</p>
          <p>
            <strong>🔗 관련 링크:</strong>
            <a :href="event.url" target="_blank" rel="noopener">자세히 보기</a>
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
      ],
      selectedRegion: "",
      events: [],
      loading: false,
      currentPage: 1,
      eventsPerPage: 5,
    };
  },
  computed: {
    paginatedEvents() {
      const start = (this.currentPage - 1) * this.eventsPerPage;
      const end = start + this.eventsPerPage;
      return this.events.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.events.length / this.eventsPerPage);
    },
  },
  methods: {
    async fetchEvents() {
      this.loading = true;
      try {
        const url = this.selectedRegion
          ? `/events/region/${encodeURIComponent(this.selectedRegion)}/`
          : `/events/`;
        const response = await axios.get(url);
        this.events = response.data;
        this.currentPage = 1;
      } catch (error) {
        console.error("Error fetching events:", error);
        this.events = [];
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchEvents();
  },
};
</script>

<style scoped>
/* 전체 레이아웃 */
.event-schedule {
  font-family: 'Noto Sans KR', sans-serif;
  color: #3a3a3a;
  background: linear-gradient(135deg, #fef7f1, #fff4e3);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease-in-out;
}

/* 헤더 */
.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.6rem;
  font-weight: bold;
  color: #ef6c57;
}

.header p {
  font-size: 1.2rem;
  color: #7a7a7a;
}

/* 지역 선택 */
.region-section {
  margin-bottom: 40px;
  text-align: center;
}

.region-label {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ef6c57;
  margin-right: 15px;
}

.region-select {
  font-size: 1rem;
  padding: 12px 15px;
  border: 2px solid #ef6c57;
  border-radius: 10px;
  background-color: #fff7f1;
  transition: border-color 0.3s, background-color 0.3s, transform 0.3s;
}

.region-select:hover {
  border-color: #d9523f;
  background-color: #ffe4d3;
  transform: scale(1.05);
}

/* 로딩 상태 */
.loading {
  text-align: center;
  font-size: 1.4rem;
  color: #ef6c57;
}

/* 데이터 없음 */
.no-data {
  text-align: center;
  font-size: 1.2rem;
  color: #999;
}

/* 행사 카드 */
.events-section ul {
  list-style: none;
  padding: 0;
}

.event-card {
  background: white;
  border: 2px solid #fcd3c1;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.4s, box-shadow 0.4s;
}

.event-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.event-card h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ef6c57;
}

.event-card p {
  font-size: 1.1rem;
  color: #555;
}

.event-card a {
  color: #d9523f;
  text-decoration: none;
  font-weight: bold;
}

.event-card a:hover {
  text-decoration: underline;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
}

.pagination button {
  background-color: #ef6c57;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 20px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.pagination button:hover {
  background-color: #d9523f;
  transform: scale(1.1);
}

.pagination button:disabled {
  background-color: #fcd3c1;
  cursor: not-allowed;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
