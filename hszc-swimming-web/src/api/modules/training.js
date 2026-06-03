import request from '@/utils/request'

export default {
  // 训练通知
  getNoticeList(params) {
    return request.get('/trainings/notices/', { params })
  },
  getNoticeDetail(id) {
    return request.get(`/trainings/notices/${id}/`)
  },
  createNotice(data) {
    return request.post('/trainings/notices/', data)
  },
  updateNotice(id, data) {
    return request.put(`/trainings/notices/${id}/`, data)
  },
  deleteNotice(id) {
    return request.delete(`/trainings/notices/${id}/`)
  },
  signUp(id, data) {
    return request.post(`/trainings/notices/${id}/sign_up/`, data)
  },
  getSignUps(id) {
    return request.get(`/trainings/notices/${id}/signups/`)
  },

  // 训练报名
  getSignUpList(params) {
    return request.get('/trainings/signups/', { params })
  },
  cancelSignUp(id) {
    return request.post(`/trainings/signups/${id}/cancel/`)
  },

  // 训练笔记
  getNoteList(params) {
    return request.get('/trainings/notes/', { params })
  },
  createNote(data) {
    return request.post('/trainings/notes/', data)
  },
  updateNote(id, data) {
    return request.put(`/trainings/notes/${id}/`, data)
  },
  deleteNote(id) {
    return request.delete(`/trainings/notes/${id}/`)
  },
  getPublicNotes() {
    return request.get('/trainings/notes/public/')
  }
}
