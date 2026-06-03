import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '工作台' }
      },
      {
        path: 'members',
        name: 'MemberList',
        component: () => import('@/views/member/List.vue'),
        meta: { title: '会员管理' }
      },
      {
        path: 'members/:id',
        name: 'MemberDetail',
        component: () => import('@/views/member/Detail.vue'),
        meta: { title: '会员详情' }
      },
      {
        path: 'competitions',
        name: 'CompetitionList',
        component: () => import('@/views/competition/List.vue'),
        meta: { title: '比赛管理' }
      },
      {
        path: 'competitions/:id',
        name: 'CompetitionDetail',
        component: () => import('@/views/competition/Detail.vue'),
        meta: { title: '比赛详情' }
      },
      {
        path: 'trainings',
        name: 'TrainingList',
        component: () => import('@/views/training/List.vue'),
        meta: { title: '训练管理' }
      },
      {
        path: 'messages',
        name: 'MessageList',
        component: () => import('@/views/message/List