<template>
  <div class="event-schedule">
    <h1>행사 일정</h1>
    <div>
      <label for="region-select">지역 선택:</label>
      <select id="region-select" v-model="selectedRegion" @change="fetchEvents">
        <option value="">모든 지역</option> <!-- 기본값으로 "모든 지역" 추가 -->
        <option v-for="region in regions" :key="region" :value="region">
          {{ region }}
        </option>
      </select>
    </div>

    <div v-if="loading">데이터를 가져오는 중...</div>

    <div v-else-if="paginatedEvents.length === 0">
      선택한 지역에 대한 행사 정보가 없습니다.
    </div>

    <div v-else>
      <ul>
        <li v-for="event in paginatedEvents" :key="event.id">
          <h3>{{ event.title }}</h3>
          <p><strong>기간:</strong> {{ event.period }}</p>
          <p><strong>지역:</strong> {{ event.region }}</p>
          <p><strong>정보:</strong> {{ event.info }}</p>
          <p>
            <strong>관련 링크: </strong>
            <a :href="event.url" target="_blank"> 더 알아보기</a>
          </p>
        </li>
      </ul>

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--">이전</button>
        <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++">다음</button>
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
      selectedRegion: "", // 선택한 지역 (기본값은 "모든 지역")
      events: [], // 전체 행사 데이터
      loading: false, // 로딩 상태
      currentPage: 1, // 현재 페이지
      eventsPerPage: 5, // 페이지당 행사 개수
    };
  },
  computed: {
    // 현재 페이지에 표시될 행사 데이터
    paginatedEvents() {
      const start = (this.currentPage - 1) * this.eventsPerPage;
      const end = start + this.eventsPerPage;
      return this.events.slice(start, end);
    },
    // 총 페이지 수
    totalPages() {
      return Math.ceil(this.events.length / this.eventsPerPage);
    },
  },
  methods: {
    async fetchEvents() {
      this.loading = true;

      try {
        // 지역 선택 여부에 따라 API 요청 URL 설정
        const url = this.selectedRegion
          ? `/events/region/${encodeURIComponent(this.selectedRegion)}/`
          : `/events/`; // 모든 지역의 행사 정보 가져오기

        const response = await axios.get(url);
        this.events = response.data; // 데이터 저장
        this.currentPage = 1; // 새로운 데이터 로드 시 페이지 초기화
      } catch (error) {
        console.error("Error fetching events:", error);
        this.events = []; // 데이터 초기화
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    // 페이지 로드 시 모든 지역의 행사 정보 불러오기
    this.fetchEvents();
  },
};
</script>

<style scoped>
.event-schedule {
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
