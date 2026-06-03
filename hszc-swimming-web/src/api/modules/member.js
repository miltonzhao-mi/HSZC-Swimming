import request from '@/utils/request'

export default {
  // 获取会员列表
  getList(params) {
    return request.get('/members/', { params })
  },
  // 获取会员详情
  getDetail(id) {
    return request.get(`/members/${id}/`)
  },
  // 创建会员
  create(data) {
    return request.post('/members/', data)
  },
  // 更新会员
  update(id, data) {
    return request.put(`/members/${id}/`, data)
  },
  // 删除会员
  delete(id) {
    return request.delete(`/members/${id}/`)
  },
  // 审批会员
  approve(id, data) {
    return request.post(`/members/${id}/approve/`, data)
  },
  // 升级会员
  upgrade(id, data) {
    return request.post(`/members/${id}/upgrade/`, data)
  },
  // 注销会员
  cancel(id) {
    return request.post(`/members/${id}/cancel/`)
  },
  // 会员统计
  getStats() {
    return request.get('/members/stats/')
  },
  // 活跃度排行
  getLeaderboard(params) {
    return request.get('/members/activities/leaderboard/', { params })
  }
}
