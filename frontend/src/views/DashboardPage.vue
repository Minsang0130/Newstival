<template>
  <div class="dashboard">
    <div class="dashboard-row">
      <div class="dashboard-block" id="wordcloud-container">
        <div class="wordcloud-title">워드클라우드</div>
        <div id="wordcloud-content" class="wordcloud-content"></div>
      </div>
      <div class="dashboard-block" id="map-container">지도</div>
    </div>
    <div class="dashboard-row">
      <div class="dashboard-block" id="barchart1-container">바 차트 1</div>
      <div class="dashboard-block" id="barchart2-container">바 차트 2</div>
    </div>
  </div>
</template>

<script>
import WordCloud from "wordcloud";
import { fetchWordCloud } from "../api/dashboard";
  
export default {
  name: "DashboardPage",
  data() {
    return {
      wordcloudData: [],  // 워드클라우드 데이터
      loading: true,
      error: null
    };
  },
  async mounted() {
    try {
      const data = await fetchWordCloud();
      this.wordcloudData = data;
      this.loading = false;
      this.renderWordCloud();
    } catch (error) {
      this.error = "워드클라우드 데이터를 로드하는 데 실패했습니다.";
      console.error("워드클라우드 데이터 로딩 중 오류 발생:", error);
      this.loading = false;
    }
  },
  methods: {
    renderWordCloud() {
      const container = document.getElementById('wordcloud-content');
      if (container && this.wordcloudData.length > 0) {
        // 다양한 색상을 정의
        const colors = ['#E53E3E', '#3182CE', '#48BB78', '#ED8936', '#9F7AEA', '#ECC94B'];

        const options = {
          list: this.wordcloudData,  // 서버에서 받아온 데이터
          gridSize: 10,
          weightFactor: (size) => size * 0.5,
          fontFamily: 'Noto Sans KR, sans-serif',
          shape: 'square',
          color: () => {
            // 색상 배열에서 무작위로 색상을 선택
            return colors[Math.floor(Math.random() * colors.length)];
          },
          rotateRatio: 0,
          rotationSteps: 2,
          backgroundColor: '#ffffff',
          minSize: 10,
          maxSize: 100
        };
        WordCloud(container, options);
      } else {
        console.error('워드클라우드 컨테이너를 찾을 수 없거나 데이터가 비어 있습니다.');
      }
    },
  },
};
</script>

<style>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dashboard-row {
  display: flex;
  gap: 20px;
}

.dashboard-block {
  flex: 1;
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  height: 300px; /* 조정 가능한 높이 */
}

#wordcloud-container {
  overflow: hidden;
  height: 350px;
  width: 100%;
  border: 1px solid #ccc;
  display: flex;
  flex-direction: column;
}

.wordcloud-title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.wordcloud-content {
  flex-grow: 1;
  overflow: visible;
  height: auto;
}
</style>
