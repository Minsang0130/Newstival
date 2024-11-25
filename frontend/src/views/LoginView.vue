<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="login-title">로그인</h1>
      <p class="login-subtitle">계정을 입력하고 로그인하세요!</p>
      <form @submit.prevent="logIn">
        <div class="form-group">
          <input
            type="text"
            v-model="username"
            class="form-input animate-input"
            placeholder="아이디"
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="password"
            class="form-input animate-input"
            placeholder="비밀번호"
          />
        </div>
        <button type="submit" class="login-button animate-button">로그인</button>
      </form>
      <div class="login-links animate-links">
        <a href="#" class="forgot-link">비밀번호를 잊으셨나요?</a>
        <a href="/signup" class="signup-link">회원가입</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';

const store = useUserStore();

const username = ref('');
const password = ref('');

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style scoped>
/* 전체 컨테이너 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ffdde1, #ee9ca7);
  font-family: 'Noto Sans KR', sans-serif;
  overflow: hidden;
  animation: fadeInBackground 2s ease-in-out;
}

/* 로그인 박스 */
.login-box {
  background: #ffffff;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 360px;
  animation: scaleIn 1s ease-in-out;
}

/* 제목 */
.login-title {
  font-size: 2rem;
  font-weight: bold;
  color: #e91e63;
  margin-bottom: 10px;
  animation: slideInDown 1s ease-out;
}

.login-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 30px;
  animation: slideInDown 1.5s ease-out;
}

/* 입력 필드 */
.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 100%; /* 버튼과 동일한 크기로 맞춤 */
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #f9f9f9;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #e91e63;
  background: #ffffff;
  box-shadow: 0 0 5px rgba(233, 30, 99, 0.3);
}

.animate-input {
  animation: fadeIn 1s ease-in-out;
}

/* 버튼 */
.login-button {
  background: #e91e63;
  color: #ffffff;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  padding: 15px;
  width: 100%; /* 입력 칸과 동일한 크기 */
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.login-button:hover {
  background: #d81b60;
  transform: translateY(-2px);
}

.login-button:active {
  transform: scale(0.98);
}

.animate-button {
  animation: bounceIn 1.5s ease;
}

/* 링크 */
.login-links {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #666;
  display: flex;
  justify-content: space-between;
  animation: fadeInUp 2s ease;
}

.forgot-link,
.signup-link {
  color: #e91e63;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.forgot-link:hover,
.signup-link:hover {
  color: #d81b60;
}

/* 애니메이션 키프레임 */
@keyframes fadeInBackground {
  0% {
    opacity: 0;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes scaleIn {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes slideInDown {
  0% {
    transform: translateY(-30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounceIn {
  0% {
    transform: scale(0.9);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
