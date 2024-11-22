import axios from "axios";

// .env 파일에서 API URL 읽기
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL,
  timeout: 5000, // 요청 타임아웃 (ms)
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청/응답 인터셉터 추가 (선택 사항)
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API 요청 실패:", error);
    return Promise.reject(error);
  }
);

export default axiosInstance;
