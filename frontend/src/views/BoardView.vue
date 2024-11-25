<template>
  <div class="festival-container">
    <!-- 헤더 -->
    <header class="festival-header">
      <h1>✏️ 축제 소식 게시판 📜</h1>
      <p>축제의 최신 정보를 확인하고 공유하세요!</p>
      <div v-if="userStore.loginUsername" class="user-panel">
        <span class="welcome-message">환영합니다, <strong>{{ userStore.loginUsername }}</strong>님 !  </span>
        <button class="create-post-btn" @click="goCreateBoard">
          ➕ 새 소식 작성
        </button>
      </div>
    </header>

    <!-- 게시판 리스트 -->
    <main class="board-section">
      <div 
        v-for="board in boardStore.boards"
        :key="board.id"
        class="board-card"
      >
        <h2 class="board-title">{{ board.title }}</h2>
        <p class="board-content">{{ board.content }}</p>
        <footer class="board-footer">
          <span>작성자: <strong>{{ board.writer }}</strong></span>
        </footer>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useBoardStore } from '@/stores/board';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userStore = useUserStore();
const boardStore = useBoardStore();

onMounted(() => {
  boardStore.getBoards();
});

const goCreateBoard = function () {
  router.push('/create-board');
};
</script>

<style scoped>
/* 전체 컨테이너 */
.festival-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 30px;
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
  border-radius: 20px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  color: #333;
  animation: fadeIn 1.5s ease-in-out;
}

/* 헤더 스타일 */
.festival-header {
  text-align: center;
  margin-bottom: 40px;
}

.festival-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #fff;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
}

.festival-header p {
  font-size: 1.2rem;
  color: 
}

.user-panel {
  margin-top: 15px;
}

.welcome-message {
  font-size: 1.1rem;
  font-weight: bold;
  color:darkslateblue
}

.create-post-btn {
  background: #ff6f61;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
  margin-top: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.create-post-btn:hover {
  background: #e6554d;
  transform: scale(1.1);
}

/* 게시판 리스트 */
.board-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
  margin-top: 30px;
}

.board-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 20px;
  text-align: left;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.board-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2);
}

.board-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ff6f61;
  margin-bottom: 15px;
}

.board-content {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.board-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #888;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
