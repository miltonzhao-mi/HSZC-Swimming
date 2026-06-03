import request from '@/utils/request'

export default {
  login(data) {
    return request.post('/users/auth/login/', data)
  },
  logout(data) {
    return request.post('/users/auth/logout/', data)
  },
  refresh(data) {
    return request.post('/users/auth/refresh/', data)
  },
  getCurrentUser() {
    return request.get('/users/auth/me/')
  }
}
