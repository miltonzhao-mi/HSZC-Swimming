<template>
  <n-layout has-sider class="app-layout">
    <!-- 侧边栏 -->
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="220"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
      class="layout-sider"
    >
      <div class="logo" :class="{ collapsed }">
        <img v-if="!collapsed" src="@/assets/images/logo.png" alt="logo" class="logo-img" />
        <span v-if="!collapsed" class="logo-text">红衫游泳</span>
      </div>
      <n-menu
        v-model:value="activeKey"
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        @update:value="handleMenuSelect"
      />
    </n-layout-sider>

    <!-- 主内容区 -->
    <n-layout>
      <!-- 顶栏 -->
      <n-layout-header bordered class="layout-header">
        <div class="header-left">
          <n-button text @click="collapsed = !collapsed">
            <n-icon :component="collapsed ? MenuOutline : Menu" />
          </n-button>
        </div>
        <div class="header-right">
          <n-dropdown :options="userMenuOptions" @select="handleUserMenuSelect">
            <div class="user-info">
              <n-avatar round size="small" :src="authStore.user?.avatar" />
              <span class="username">{{ authStore.user?.username }}</span>
            </div>
          </n-dropdown>
        </div>
      </n-layout-header>

      <!-- 内容 -->
      <n-layout-content class="layout-content">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Menu, MenuOutline, PersonOutline, LogOutOutline } from '@vicons/ionicons5'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const collapsed = ref(false)
const activeKey = computed(() => route.name)

const menuOptions = [
  {
    label: '工作台',
    key: 'Dashboard',
    icon: () => h('i', { class: 'n-icon n-icon-grid' })
  },
  {
    label: '会员管理',
    key: 'MemberList',
    icon: () => h('i', { class: 'n-icon n-icon-people' })
  },
  {
    label: '比赛管理',
    key: 'CompetitionList',
    icon: () => h('i', { class: 'n-icon n-icon-trophy' })
  },
  {
    label: '训练管理',
    key: 'TrainingList',
    icon: () => h('i', { class: 'n-icon n-icon-fitness' })
  },
  {
    label: '消息中心',
    key: 'MessageList',
    icon: () => h('i', { class: 'n-icon n-icon-mail' })
  }
]

const userMenuOptions = [
  { label: '个人中心', key: 'profile', icon: PersonOutline },
  { label: '退出登录', key: 'logout', icon: LogOutOutline }
]

function handleMenuSelect(key) {
  router.push({ name: key })
}

function handleUserMenuSelect(key) {
  if (key === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.layout-sider {
  background: #fff;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #f0f0f0;
}

.logo.collapsed {
  justify-content: center;
}

.logo-img {
  height: 32px;
  margin-right: 8px;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #1890ff;
}

.layout-header {
  height: 60px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
}

.layout-content {
  padding: 16px;
  background: #f5f5f5;
}
</style>
