// django 의 urls.py 역할
// 사용자가 특정 경로로 들어오면, 
// 해당하는 컴포넌트(페이지)를 출력해줄 수 있도록 설정해주는 파일
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import BoardCreateView from '@/views/BoardCreateView.vue'
import BoardView from '../views/BoardView.vue';
import EventScheduleView from '@/views/EventScheduleView.vue'
import DashboardPage from '../views/DashboardPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/events', // 새로운 경로
      name: 'events',
      component: EventScheduleView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/create-board',
      name: 'createBorad',
      component: BoardCreateView,
    },
    {
      path: '/board',
      name: 'Board',
      component: BoardView, // 새 라우트 추가
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: DashboardPage, // 대시보드 페이지 컴포넌트
    },
  ],
})

export default router
