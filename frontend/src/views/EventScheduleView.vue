<template>
    <div class="event-schedule">
      <h1>행사 일정</h1>
      <div class="event-list">
        <ul>
          <li v-for="event in events" :key="event.id">
            <h3>{{ event.title }}</h3>
            <p>{{ event.date }} - {{ event.location }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        events: [
          // 예시 데이터
          { id: 1, title: '전주 국제 영화제', date: '2024-12-01', location: '전라북도 전주시' },
          { id: 2, title: '부산 불꽃축제', date: '2024-12-10', location: '부산광역시' },
          { id: 3, title: '강릉 커피 축제', date: '2024-12-15', location: '강원도 강릉시' },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .event-schedule {
    padding: 20px;
  }
  
  .event-list ul {
    list-style: none;
    padding: 0;
  }
  
  .event-list li {
    margin: 10px 0;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 4px;
  }
  </style>
  