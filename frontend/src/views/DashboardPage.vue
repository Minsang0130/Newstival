<template>
  <div class="dashboard">
    <!-- 첫 번째 행: 워드클라우드와 지도 -->
    <div class="dashboard-row">
      <div class="dashboard-block" id="wordcloud-container">
        <div class="wordcloud-title">
          워드클라우드
          <select v-model="selectedRegion" @change="updateWordCloud">
            <option value="all">전체</option>
            <option value="전라북도">전라북도</option>
            <option value="전라남도">전라남도</option>
            <option value="충청남도">충청남도</option>
            <option value="경상북도">경상북도</option>
            <option value="경상남도">경상남도</option>
            <option value="강원도">강원도</option>
            <option value="부산시">부산시</option>
            <option value="서울시">서울시</option>
            <option value="인천시">인천시</option>
            <option value="경기도">경기도</option>
            <option value="대전시">대전시</option>
          </select>
        </div>
        <div id="wordcloud-content" class="wordcloud-content"></div>
      </div>
      <div class="dashboard-block" id="map-container">
        <div class="map-title">지도</div>
        <div id="map"></div>
      </div>
    </div>
    <!-- 두 번째 행: 바 차트 1과 바 차트 2 -->
    <div class="dashboard-row">
      <div class="dashboard-block" id="barchart1-container">
        <div class="chart-title">바차트1 제목</div>
        <div id="barchart1-content"></div>
      </div>
      <div class="dashboard-block" id="barchart2-container">바 차트 2</div>
    </div>
  </div>
</template>

<script>
import WordCloud from "wordcloud";
import { fetchWordCloud, fetchHeatmap, fetchTopRegions } from "../api/dashboard";
import * as d3 from "d3";
import * as topojson from "topojson";
import southKoreaMap from "../assets/south-korea-map.json";

export default {
  name: "DashboardPage",
  data() {
    return {
      wordcloudData: [],
      selectedRegion: 'all', // 기본값 설정
      loading: true,
      error: null,
      heatmapData: [], // 히트맵 데이터
      topRegionsData: [], // TOP 3 지역 데이터
    };
  },
  async mounted() {
    await this.updateWordCloud();
    try {
      const heatmapData = await fetchHeatmap();
      if (Array.isArray(heatmapData)) {
        this.heatmapData = heatmapData;
        this.renderHeatmap();
      } else {
        throw new Error("히트맵 데이터가 배열 형태가 아닙니다.");
      }
    } catch (error) {
      this.error = "히트맵 데이터를 로드하는 데 실패했습니다.";
      console.error("히트맵 데이터 로딩 중 오류 발생:", error);
    }

    try {
      const topRegionsData = await fetchTopRegions();
      if (Array.isArray(topRegionsData)) {
        this.topRegionsData = topRegionsData;
        this.renderBarChart();
      } else {
        throw new Error("TOP 3 지역 데이터가 배열 형태가 아닙니다.");
      }
    } catch (error) {
      console.error("TOP 3 지역 데이터 로딩 중 오류 발생:", error);
    }
  },
  methods: {
    async updateWordCloud() {
      try {
        const wordCloudData = await fetchWordCloud(this.selectedRegion);
        if (Array.isArray(wordCloudData)) {
          this.wordcloudData = wordCloudData;
          this.renderWordCloud();
        } else {
          throw new Error("워드클라우드 데이터가 배열 형태가 아닙니다.");
        }
      } catch (error) {
        this.error = "워드클라우드 데이터를 로드하는 데 실패했습니다.";
        console.error("워드클라우드 데이터 로딩 중 오류 발생:", error);
      }
    },
    renderWordCloud() {
      const container = document.getElementById("wordcloud-content");
      if (container && this.wordcloudData.length > 0) {
        const containerWidth = container.offsetWidth; // 컨테이너 너비
        const containerHeight = container.offsetHeight; // 컨테이너 높이
        const maxFrequency = Math.max(...this.wordcloudData.map(([_, size]) => size)); // 가장 높은 빈도

        const colors = [
            "#E53E3E",
            "#3182CE",
            "#48BB78",
            "#ED8936",
            "#9F7AEA",
            "#ECC94B",
        ];

        const options = {
            list: this.wordcloudData,
            gridSize: Math.round(containerWidth / 50), // 컨테이너 크기에 비례하여 그리드 설정
            weightFactor: (size) => (size / maxFrequency) * (containerWidth / 5), // 컨테이너 크기를 기준으로 글씨 크기 조정
            fontFamily: "Noto Sans KR, sans-serif",
            shape: "square",
            color: () => colors[Math.floor(Math.random() * colors.length)],
            rotateRatio: 0,
            rotationSteps: 2,
            backgroundColor: "#ffffff",
            minSize: 30, // 단어 최소 크기
            maxSize: Math.min(containerWidth, containerHeight) / 5, // 단어 최대 크기를 컨테이너 크기에 비례하여 설정
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
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('ko-KR', options);
    },
    renderBarChart() {
      const container = d3.select("#barchart1-content");
      const width = container.node().offsetWidth || 600;
      const height = 360;
      const margin = { top: 20, right: 30, bottom: 50, left: 40 };

      const svg = container
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet");

      const x = d3
        .scaleBand()
        .domain(this.topRegionsData.map(d => d.main_region))
        .range([margin.left, width - margin.right])
        .padding(0.1);

      const y = d3
        .scaleLinear()
        .domain([0, d3.max(this.topRegionsData, d => d.count)])
        .nice()
        .range([height - margin.bottom, margin.top]);

      svg
        .append("g")
        .selectAll("rect")
        .data(this.topRegionsData)
        .enter()
        .append("rect")
        .attr("x", d => x(d.main_region))
        .attr("y", d => y(d.count))
        .attr("height", d => y(0) - y(d.count))
        .attr("width", x.bandwidth())
        .attr("fill", "#3182CE");

      svg
        .append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .style("font-weight", "bold")
        .style("font-size", "20px");

      svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(d3.max(this.topRegionsData, d => d.count)))
        .selectAll("text")
        .style("font-size", "16px");

      // Update the chart title with the current date
      const today = new Date();
      const formattedDate = this.formatDate(today);
      document.querySelector('.chart-title').textContent = `${formattedDate} 기사 수 TOP3`;
    },
  },
};
</script>

<style>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  color: #000;
  text-align: center;
}

.dashboard-row {
  display: flex;
  gap: 20px;
  width: 100%;
}

.dashboard-block {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 20px;
  box-sizing: border-box;
  height: 400px;
  display: flex;
  flex-direction: column;
  flex: 1;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.dashboard-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.chart-title, .map-title, .wordcloud-title {
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  background-color: #ffe0e0;
  border-bottom: 1px solid #fcd3c1;
  color: #000;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
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
  object-fit: contain;
}

#barchart1-container,
#barchart2-container {
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 10px;
  box-sizing: border-box;
  height: 400px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.chart-title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.map-title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

#barchart1-container text {
  fill: #000;
}

</style>
