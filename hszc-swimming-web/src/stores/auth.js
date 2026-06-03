import { defineStore } from 'pinia'
import { getUser, clearAuth } from '@/utils/storage'
import { getToken, setToken } from '@/utils/storage'
import authApi from '@/api/modules/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: getUser(),
    token: getToken(),
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    userType: (state) => state.user?.user_type || 'member',
  },

  actions: {
    async login(username, password) {
      const res = await authApi.login({ username, password })
      setToken(res.data.access)
      this.token = res.data.access
      this.user = res.data.user
      return res
    },

    logout() {
      clearAuth()
      this.user = null
      this.token = null
    },

    async refreshToken() {
      const res = await authApi.refresh({ refresh: this.token })
      setToken(res.data.access)
      this.token = res.data.access