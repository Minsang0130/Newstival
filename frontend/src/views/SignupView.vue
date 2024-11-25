<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1 class="signup-title">회원가입</h1>
      <p class="signup-subtitle">계정을 생성하고 서비스를 이용하세요!</p>
      <form @submit.prevent="signUp">
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
            v-model="password1"
            class="form-input animate-input"
            placeholder="비밀번호"
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="password2"
            class="form-input animate-input"
            placeholder="비밀번호 확인"
          />
        </div>
        <button type="submit" class="signup-button animate-button">회원가입</button>
      </form>
      <div class="signup-links animate-links">
        <p>이미 계정이 있으신가요?</p>
        <a href="/login" class="login-link">로그인</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';

const store = useUserStore();

const username = ref('');
const password1 = ref('');
const password2 = ref('');

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  };
  store.signUp(payload);
};
</script>

<style scoped>
/* 전체 컨테이너 */
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #d4fc79, #96e6a1);
  font-family: 'Noto Sans KR', sans-serif;
  overflow: hidden;
  animation: fadeInBackground 2s ease-in-out;
}

/* 회원가입 박스 */
.signup-box {
  background: #ffffff;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 400px;
  animation: scaleIn 1s ease-in-out;
}

/* 제목 */
.signup-title {
  font-size: 2rem;
  font-weight: bold;
  color: #4caf50;
  margin-bottom: 10px;
}

.signup-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 30px;
}

/* 입력 필드 */
.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 100%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #f9f9f9;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #4caf50;
  background: #ffffff;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

.animate-input {
  animation: fadeIn 1s ease-in-out;
}

/* 버튼 */
.signup-button {
  background: #4caf50;
  color: #ffffff;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  padding: 15px;
  width: 100%;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.signup-button:hover {
  background: #43a047;
  transform: translateY(-2px);
}

.signup-button:active {
  transform: scale(0.98);
}

.animate-button {
  animation: bounceIn 1.5s ease;
}

/* 링크 */
.signup-links {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #666;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

.signup-links p {
  margin: 0;
  color: #666;
}

.login-link {
  color: #4caf50;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.login-link:hover {
  color: #388e3c;
}

/* 애니메이션 */
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
