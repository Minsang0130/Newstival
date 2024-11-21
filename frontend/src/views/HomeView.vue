<<<<<<< HEAD
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

<template>
  <div class="festival-container">
    <!-- 헤더 -->
    <header class="festival-header">
      <h1>🎉 축제 소식 게시판 🎉</h1>
      <p>축제의 최신 정보를 확인하고 공유하세요!</p>
      <div v-if="userStore.loginUsername" class="user-panel">
        <span class="welcome-message">환영합니다, {{ userStore.loginUsername }}님! 🌟</span>
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
          <span>작성자: {{ board.writer }}</span>
          <span>#{{ board.id }}</span>
        </footer>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 축제 컨테이너 */
.festival-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  animation: fadeIn 1.5s ease-in-out;
  color: #fff;
  text-align: center;
}

/* 헤더 */
.festival-header {
  margin-bottom: 30px;
}

.festival-header h1 {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #fff;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
}

.festival-header p {
  font-size: 18px;
  color: #ffe0e0;
}

.user-panel {
  margin-top: 15px;
}

.welcome-message {
  font-size: 16px;
  font-weight: bold;
  color: #fff;
}

.create-post-btn {
  background: #ff6f61;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
  margin-top: 10px;
}

.create-post-btn:hover {
  background: #e6554d;
  transform: scale(1.1);
}

/* 게시판 리스트 */
.board-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.board-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 20px;
  text-align: left;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.board-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.board-title {
  font-size: 22px;
  font-weight: bold;
  color: #ff6f61;
  margin-bottom: 10px;
}

.board-content {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

.board-footer {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
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
=======
<script setup>
import { useUserStore } from '@/stores/user'
import { useBoardStore } from '@/stores/board'
// setup: 아직 틀(DOM)이 완성되지 않음
// onMounted: 라이프 사이클 훅
//    데이터가 그려질 틀(DOM)이 완성되고 난 후 시점
// API 를 통해 데이터를 가져오는 시점
//  -> 틀이 완성되고 난 후
//  -> onMounted 안에 작성해주어야 한다.
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const userStore = useUserStore()
const boardStore = useBoardStore()

onMounted(() => {
  boardStore.getBoards()
})

const goCreateBoard = function() {
  router.push('/create-board')
}
</script>

<template>
  <div>
    <h1>게시글 출력</h1>
    <p v-if="userStore.loginUsername">로그인된 사용자: {{ userStore.loginUsername }}</p>
    <button 
      v-if="userStore.loginUsername"
      @click="goCreateBoard"
    >게시글 생성하기</button>
    <div 
      v-for="board in boardStore.boards"
      :key="board.id"
      >
      <p>{{ board.id }}번째 글</p>
      <p>제목: {{ board.title }}</p>
      <p>내용: {{ board.content }}</p>
      <p>작성자: {{ board.writer }}</p>
      <hr>
    </div>
  </div>
</template>

<style scoped>

</style>
>>>>>>> cd4cc6661f9202082f64f3adf3e24c368fdf58ff
