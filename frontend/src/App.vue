<script setup>
import { useUserStore } from '@/stores/user';

const store = useUserStore();

const handleLogout = () => {
  store.logOut();
};
</script>

<template>
  <header class="header">
    <nav class="nav">
      <RouterLink to="/">메인 페이지</RouterLink> |
      <RouterLink to="/board">게시판</RouterLink> |
      <RouterLink to="/dashboard">대시보드</RouterLink> |
      <RouterLink to="/events">행사일정</RouterLink>
    </nav>
    <div class="user-status">
      <!-- 로그인 상태 -->
      <span v-if="store.token">
        환영합니다, <strong>{{ store.loginUsername }}</strong>님!
        <span class="logout-link" @click="handleLogout">[로그아웃]</span>
      </span>
      <!-- 로그아웃 상태 -->
      <span v-else>
        <RouterLink to="/login">로그인 필요</RouterLink>
      </span>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
/* 헤더 스타일 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ddd;
}

/* 네비게이션 스타일 */
.nav {
  display: flex;
  gap: 15px;
}

.nav a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
  transition: color 0.3s;
}

.nav a:hover {
  color: #e91e63;
}

/* 사용자 상태 표시 스타일 */
.user-status {
  font-size: 0.9rem;
  color: #666;
}

.user-status strong {
  color: #e91e63;
}

.logout-link {
  cursor: pointer;
  color: #e91e63;
  font-weight: bold;
  margin-left: 5px;
  transition: color 0.3s;
}

.logout-link:hover {
  color: #c2185b;
}
</style>
