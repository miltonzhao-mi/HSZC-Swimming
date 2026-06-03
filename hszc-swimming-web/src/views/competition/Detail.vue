<template>
  <div class="competition-detail">
    <n-card title="比赛详情">
      <n-descriptions bordered :column="2">
        <n-descriptions-item label="比赛名称">{{ competition.name }}</n-descriptions-item>
        <n-descriptions-item label="地点">{{ competition.location }}</n-descriptions-item>
        <n-descriptions-item label="开始日期">{{ competition.start_date }}</n-descriptions-item>
        <n-descriptions-item label="结束日期">{{ competition.end_date }}</n-descriptions-item>
        <n-descriptions-item label="报名截止">{{ competition.sign_up_deadline }}</n-descriptions-item>
        <n-descriptions-item label="状态">{{ getStatusText(competition.status) }}</n-descriptions-item>
      </n-descriptions>

      <n-tabs type="line" style="margin-top: 24px">
        <n-tab-pane name="signups" title="参赛报名">
          <n-data-table :columns="signupColumns" :data="signups" :loading="loading" />
        </n-tab-pane>
        <n-tab-pane name="scores" title="成绩录入">
          <n-data-table :columns="scoreColumns" :data="scores" :loading="scoresLoading" />
        </n-tab-pane>
        <n-tab-pane name="files" title="成绩册">
          <n-space style="margin-bottom: 16px">
            <n-upload :action="`/api/v1/competitions/files/`" :data="{ competition: competitionId }" :headers="{ Authorization: `Bearer ${token}` }" @finish="handleUploadFinish">
              <n-button>上传成绩册</n-button>
            </n-upload>
          </n-space>
          <n-data-table :columns="fileColumns" :data="scoreFiles" />
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCompetitionDetail, getCompetitionSignUps, getScoreList, getScoreFiles } from '@/api/modules/competition'
import { getToken } from '@/utils/storage'

const route = useRoute()
const competitionId = route.params.id
const token = getToken()
const competition = ref({})
const signups = ref([])
const scores = ref([])
const scoreFiles = ref([])
const loading = ref(false)
const scoresLoading = ref(false)

const signupColumns = [
  { title: '姓名', key: 'member_name' },
  { title: '参赛项目', key: 'event_item' },
  { title: '距离', key: 'distance' },
  { title: '报名时间', key: 'signup_time' },
  { title: '渠道', key: 'register_by', render: (row) => row.register_by === 'miniapp' ? '小程序' : 'PC端' }
]

const scoreColumns = [
  { title: '姓名', key: 'member_name' },
  { title: '项目', key: 'event_item' },
  { title: '成绩', key: 'score_time', render: (row) => `${row.score_time}s` },
  { title: '名次', key: 'rank' },
  { title: '积分', key: 'points' }
]

const fileColumns = [
  { title: '文件名', key: 'name' },
  { title: '上传人', key: 'uploaded_by_name' },
  { title: '上传时间', key: 'uploaded_at' },
  { title: '操作', key: 'action', render: (row) => {
    return h('a', { href: row.file, target: '_blank', style: { color: '#1890ff' } }, '查看')
  }}
]

function getStatusText(status) {
  const map = { preparing: '筹备中', registration: '报名中', ongoing: '进行中', finished: '已结束' }
  return map[status] || status
}

function handleUploadFinish() {
  loadScoreFiles()
}

async function loadScoreFiles() {
  try {
    const res = await getScoreFiles({ competition: competitionId })
    scoreFiles.value = res.data.items || []
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  try {
    loading.value = true
    const res = await getCompetitionDetail(competitionId)
    competition.value = res.data

    const signupRes = await getCompetitionSignUps(competitionId)
    signups.value = signupRes.data || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
  loadScoreFiles()
})
</script>
