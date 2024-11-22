<template>
  <div class="dashboard">
    <!-- 첫 번째 행: 워드클라우드와 지도 -->
    <div class="dashboard-row">
      <div class="dashboard-block" id="wordcloud-container">
        <div class="wordcloud-title">워드클라우드</div>
        <div id="wordcloud-content" class="wordcloud-content"></div>
      </div>
      <div class="dashboard-block" id="map-container">
        <div class="map-title">지도</div>
        <div id="map"></div>
      </div>
    </div>
    <!-- 두 번째 행: 바 차트 1과 바 차트 2 -->
    <div class="dashboard-row">
      <div class="dashboard-block" id="barchart1-container">바 차트 1</div>
      <div class="dashboard-block" id="barchart2-container">바 차트 2</div>
    </div>
  </div>
</template>




<script>
import WordCloud from "wordcloud";
import { fetchWordCloud, fetchHeatmap } from "../api/dashboard";
import * as d3 from "d3";
import * as topojson from "topojson";
import southKoreaMap from "../assets/south-korea-map.json";

export default {
  name: "DashboardPage",
  data() {
    return {
      wordcloudData: [], // 워드클라우드 데이터
      loading: true,
      error: null,
      heatmapData: [], // 히트맵 데이터
    };
  },
  async mounted() {
    // 워드클라우드 데이터 로드
    try {
      const data = await fetchWordCloud();
      if (Array.isArray(data)) {
        this.wordcloudData = data;
        this.loading = false;
        this.renderWordCloud();
      } else {
        throw new Error("워드클라우드 데이터가 배열 형태가 아닙니다.");
      }
    } catch (error) {
      this.error = "워드클라우드 데이터를 로드하는 데 실패했습니다.";
      console.error("워드클라우드 데이터 로딩 중 오류 발생:", error);
      this.loading = false;
    }

    // 히트맵 데이터 로드
    try {
      const data = await fetchHeatmap();
      if (Array.isArray(data)) {
        this.heatmapData = data;
        this.renderHeatmap();
      } else {
        throw new Error("히트맵 데이터가 배열 형태가 아닙니다.");
      }
    } catch (error) {
      this.error = "히트맵 데이터를 로드하는 데 실패했습니다.";
      console.error("히트맵 데이터 로딩 중 오류 발생:", error);
    }
  },
  methods: {
    renderWordCloud() {
      const container = document.getElementById("wordcloud-content");
      if (container && this.wordcloudData.length > 0) {
        const colors = [
          "#E53E3E",
          "#3182CE",
          "#48BB78",
          "#ED8936",
          "#9F7AEA",
          "#ECC94B",
        ];

        const options = {
          list: this.wordcloudData, // 서버에서 받아온 데이터
          gridSize: 3,
          weightFactor: (size) => size * 0.5,
          fontFamily: "Noto Sans KR, sans-serif",
          shape: "square",
          color: () => colors[Math.floor(Math.random() * colors.length)],
          rotateRatio: 0,
          rotationSteps: 2,
          backgroundColor: "#ffffff",
          minSize: 10,
          maxSize: 100,
        };
        WordCloud(container, options);
      } else {
        console.error("워드클라우드 컨테이너를 찾을 수 없거나 데이터가 비어 있습니다.");
      }
    },
    async fetchHeatmapData() {
    try {
      const response = await fetch("http://127.0.0.1:8000/dashboard/heatmap/");
      if (!response.ok) {
        throw new Error("Failed to fetch heatmap data");
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching heatmap data:", error);
      return [];
    }
  },

  async renderHeatmap() {
    const mapContainer = document.getElementById('map');
    const width = mapContainer.offsetWidth;
    const height = mapContainer.offsetHeight;

    // SVG 생성
    const svg = d3
      .select("#map")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    // 지도 투영 설정
    const projection = d3
      .geoMercator()
      .center([128, 36])
      .scale(3000)
      .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);

    // 서버에서 데이터 가져오기
    const heatmapData = await this.fetchHeatmapData();

    if (
      !heatmapData.every(
        (item) => "main_region" in item && "count" in item
      )
    ) {
      console.error("Invalid data format:", heatmapData);
      return;
    }

    // 권역별 데이터 매핑
    const regionCounts = heatmapData.reduce((acc, curr) => {
      acc[curr.main_region] = curr.count;
      return acc;
    }, {});

    // 지도에 GeoJSON 데이터 적용
    svg
      .selectAll("path")
      .data(southKoreaMap.features)
      .enter()
      .append("path")
      .attr("d", path)
      .attr("fill", (d) => {
        const region = d.properties.name; // GeoJSON 내 권역 이름
        const count = regionCounts[region] || 0; // 권역별 뉴스 개수
        // 색상 그라데이션
        return count > 0 ? `rgba(255, 0, 0, ${Math.min(count / 10, 1)})` : "#e0e0e0";
      })
      .attr("stroke", "#000");

    // 권역별 뉴스 데이터 개수 텍스트 표시
    svg
      .selectAll("text")
      .data(southKoreaMap.features)
      .enter()
      .append("text")
      .attr("transform", (d) => {
        const centroid = path.centroid(d);
        return `translate(${centroid[0]}, ${centroid[1]})`;
      })
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .style("font-size", "12px")
      .text((d) => {
        const region = d.properties.name;
        return regionCounts[region] || "";
      });
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
  width: 100%;
}

.dashboard-block {
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 10px;
  box-sizing: border-box;
  height: 400px; /* 고정된 높이 */
  display: flex;
  flex-direction: column;
  flex: 1; /* 각 블록이 동일한 너비를 가지도록 설정 */
}

#wordcloud-container {
  overflow: hidden;
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
  overflow: hidden;
}

#map-container {
  display: flex;
  flex-direction: column;
}

#map {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: contain; /* 지도 내용이 영역 안에 맞춰지도록 설정 */
}

#barchart1-container,
#barchart2-container {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f4f4f4;
  height: 100%;
}

.map-title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

</style>
