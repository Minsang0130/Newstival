import axiosInstance from './axiosInstance';

// 백엔드 기본 URL 설정
const BASE_URL = 'http://127.0.0.1:8000';  // Django 서버의 기본 포트가 8000입니다

// 워드클라우드 데이터 가져오기
export const fetchWordCloud = async (region) => {
  try {
    const response = await axiosInstance(`${BASE_URL}/dashboard/wordcloud/`, {
      params: { region },
    });
    return response.data;
  } catch (error) {
    console.error('워드클라우드 데이터 가져오기 실패:', error);
    throw error;
  }
};


// 히트맵 데이터 가져오기
export const fetchHeatmap = async () => {
  try {
    const response = await axiosInstance.get(`${BASE_URL}/dashboard/heatmap/`);
    return response.data;
  } catch (error) {
    console.error('히트맵 데이터 가져오기 실패:', error);
    throw error;
  }
};

// TOP 3 지역 뉴스 바차트 데이터
export const fetchTopRegions = async () => {
  try {
    const response = await axiosInstance.get(`${BASE_URL}/dashboard/top-regions/`);
    return response.data;
  } catch (error) {
    console.error('TOP 3 지역 데이터 가져오기 실패:', error);
    throw error;
  }
};

// 오늘 가장 많이 본 뉴스 데이터
export const fetchTopNews = async () => {
  const response = await axiosInstance.get(`/dashboard/top-news`);
  return response.data;
};
