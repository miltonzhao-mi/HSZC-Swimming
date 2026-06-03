import request from './request'

// 会员管理
export const getMemberList = (params) => request.get('/members/', { params })
export const getMemberDetail = (id) => request.get(`/members/${id}/`)
export const createMember = (data) => request.post('/members/', data)
export const updateMember = (id, data) => request.put(`/members/${id}/`, data)
export const deleteMember = (id) => request.delete(`/members/${id}/`)
export const importMembers = (data) => request.post('/members/import_excel/', data)
export const approveMember = (id, data) => request.post(`/members/${id}/approve/`, data)
export const upgradeMember = (id, data) => request.post(`/members/${id}/upgrade/`, data)
export const cancelMember = (id) => request.post(`/members/${id}/cancel/`)
export const getMemberStats = () => request.get('/members/stats/')

// 比赛管理
export const getCompetitionList = (params) => request.get('/competitions/', { params })
export const getCompetitionDetail = (id) => request.get(`/competitions/${id}/`)
export const createCompetition = (data) => request.post('/competitions/', data)
export const updateCompetition = (id, data) => request.put(`/competitions/${id}/`, data)
export const deleteCompetition = (id) => request.delete(`/competitions/${id}/`)
export const signUpCompetition = (id, data) => request.post(`/competitions/${id}/sign_up/`, data)
export const getCompetitionSignUps = (id) => request.get(`/competitions/${id}/signups/`)

// 参赛报名
export const getSignUpList = (params) => request.get('/competitions/signups/', { params })
export const cancelSignUp = (id) => request.post(`/competitions/signups/${id}/cancel/`)

// 成绩管理
export const getScoreList = (params) => request.get('/competitions/scores/', { params })
export const getMemberBestScore = (params) => request.get('/competitions/scores/member_best/', { params })
export const createScore = (data) => request.post('/competitions/scores/', data)

// 训练管理
export const getTrainingNoticeList = (params) => request.get('/trainings/notices/', { params })
export const createTrainingNotice = (data) => request.post('/trainings/notices/', data)
export const updateTrainingNotice = (id, data) => request.put(`/trainings/notices/${id}/`, data)
export const deleteTrainingNotice = (id) => request.delete(`/trainings/notices/${id}/`)
export const signUpTraining = (id, data) => request.post(`/trainings/notices/${id}/sign_up/`, data)
export const getTrainingSignUps = (id) => request.get(`/trainings/notices/${id}/signups/`)

// 训练笔记
export const getTrainingNoteList = (params) => request.get('/trainings/notes/', { params })
export const createTrainingNote = (data) => request.post('/trainings/notes/', data)
export const updateTrainingNote = (id, data) => request.put(`/trainings/notes/${id}/`, data)
export const deleteTrainingNote = (id) => request.delete(`/trainings/notes/${id}/`)

// 消息中心
export const getMessageList = (params) => request.get('/messages/', { params })
export const createMessage = (data) => request.post('/messages/', data)
export const markMessageRead = (id) => request.post(`/messages/${id}/read/`)
export const getUnreadCount = () => request.get('/messages/unread_count/')
