<script setup>
import { ref } from 'vue';
import { useBoardStore } from '@/stores/board';

const boardStore = useBoardStore();

const title = ref('');
const content = ref('');

const createBoard = function () {
  const payload = {
    title: title.value,
    content: content.value,
  };
  boardStore.createBoard(payload);
};
</script>

<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1 class="signup-title">게시글 생성</h1>
      <p class="signup-subtitle">새로운 게시글을 작성해보세요!</p>
      <form @submit.prevent="createBoard">
        <div class="form-group">
          <input
            type="text"
            v-model="title"
            class="form-input animate-input"
            placeholder="제목을 입력하세요"
          />
        </div>
        <div class="form-group">
          <textarea
            v-model="content"
            class="form-input animate-input"
            placeholder="내용을 입력하세요"
            rows="5"
          ></textarea>
        </div>
        <button type="submit" class="signup-button animate-button">
          게시글 생성하기
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* signup.vue 스타일 재사용 */
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

.signup-box {
  background: #ffffff;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 400px;
  animation: scaleIn 1s ease-in-out;
}

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

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 85%;
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

textarea {
  resize: none;
}

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
</style>
