<template>
  <div class="event-schedule">
    <h1>행사 일정</h1>
    <div>
      <label for="region-select">지역 선택:</label>
      <select id="region-select" v-model="selectedRegion" @change="fetchEvents">
        <option disabled value="">지역을 선택하세요</option>
        <option v-for="region in regions" :key="region" :value="region">
          {{ region }}
        </option>
      </select>
    </div>

    <div v-if="loading">데이터를 가져오는 중...</div>

    <div v-else-if="events.length === 0">
      선택한 지역에 대한 행사 정보가 없습니다.
    </div>

    <div v-else>
      <ul>
        <li v-for="event in events" :key="event.id">
          <h3>{{ event.title }}</h3>
          <p><strong>기간:</strong> {{ event.period }}</p>
          <p><strong>지역:</strong> {{ event.region }}</p>
          <p><strong>정보:</strong> {{ event.info }}</p>
          <p>
            <strong>관련 링크:</strong>
            <a :href="event.url" target="_blank">더 알아보기</a>
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
      selectedRegion: "", // 선택한 지역
      events: [], // 행사 데이터
      loading: false, // 로딩 상태
    };
  },
  methods: {
    async fetchEvents() {
      if (!this.selectedRegion) return;

      this.loading = true;
      try {
        const response = await axios.get(
          `/events/region/${encodeURIComponent(this.selectedRegion)}/`
        );
        this.events = response.data; // 데이터 저장
      } catch (error) {
        console.error("Error fetching events:", error);
        this.events = []; // 데이터 초기화
      } finally {
        this.loading = false;
      }
    },
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
</style>
