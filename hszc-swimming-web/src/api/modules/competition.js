import request from '@/utils/request'

export default {
  // 比赛列表
  getList(params) {
    return request.get('/competitions/', { params })
  },
  // 比赛详情
  getDetail(id) {
    return request.get(`/competitions/${id}/`)
  },
  // 创建比赛
  create(data) {
    return request.post('/competitions/', data)
  },
  // 更新比赛
  update(id, data) {
    return request.put(`/competitions/${id}/`, data)
  },
  // 删除比赛
  delete(id) {
    return request.delete(`/competitions/${id}/`)
  },
  // 参赛报名
  signUp(id, data) {
    return request.post(`/competitions/${id}/sign_up/`, data)
  },
  // 获取报名列表
  getSignUps(id) {
    return request.get(`/competitions/${id}/signups/`)
  },
  // 批量导入报名
  importSignUps(id, data) {
    return request.post(`/competitions/${id}/import_signups/`, data)
  },

  // 报名管理
  getSignUpList(params) {
    return request.get('/competitions/signups/', { params })
  },
  cancelSignUp(id) {
    return request.post(`/competitions/signups/${id}/cancel/`)
  },

  // 成绩管理
  getScoreList(params) {
    return request.get('/competitions/scores/', { params })
  },
  createScore(data) {
    return request.post('/competitions/scores/', data)
  },
  getMemberBestScore(params) {
    return request.get('/competitions/scores/member_best/', { params })
  },

  // 成绩册
  getScoreFiles(params) {
    return request.get('/competitions/files/', { params })
  },
  uploadScoreFile(data) {
    return request.post('/competitions/files/', data)
  },

  // 比赛项目
  getEventItems() {
    return request.get('/competitions/items/')
  },
  getEventDistances() {
    return request.get('/competitions/items/distances/')
  }
}
