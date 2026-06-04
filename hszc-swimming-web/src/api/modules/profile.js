import request from '@/utils/request'

export default {
  // 会员画像摘要
  getSummary(member_id) {
    return request.get('/profiles/member/summary/', { params: { member_id } })
  },

  // 成绩趋势
  getPerformanceTrend(params) {
    return request.get('/profiles/member/performance_trend/', { params })
  },

  // 个人最佳成绩
  getPersonalBests(member_id) {
    return request.get('/profiles/member/personal_bests/', { params: { member_id } })
  },

  // 活跃度排行榜
  getLeaderboard(params) {
    return request.get('/profiles/member/leaderboard/', { params })
  },

  // 会员统计概览
  getStatistics() {
    return request.get('/profiles/member/statistics/')
  },

  // 成绩记录列表
  getRecordList(params) {
    return request.get('/profiles/records/', { params })
  },

  // 同步成绩记录
  syncFromScores(member_id) {
    return request.post('/profiles/records/sync_from_scores/', { member_id })
  }
}