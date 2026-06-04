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
        path: 'members/:id/profile',
        name: 'MemberProfile',
        component: () => import('@/views/profile/Profile.vue'),
        meta: { title: '会员画像' }
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
        component: () => import('@/views/message/List.vue'),
        meta: { title: '消息中心' }
      },
      {
        path: 'leaderboard',
        name: 'Leaderboard',
        component: () => import('@/views/profile/Leaderboard.vue'),
        meta: { title: '活跃度排行' }
      },
      {
        path: 'standards',
        name: 'StandardList',
        component: () => import('@/views/standards/List.vue'),
        meta: { title: '等级标准' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 北京红衫` : '北京红衫'

  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router