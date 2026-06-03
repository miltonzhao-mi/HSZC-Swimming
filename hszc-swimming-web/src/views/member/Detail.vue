<template>
  <div class="member-detail">
    <n-card title="会员详情">
      <n-descriptions bordered :column="2">
        <n-descriptions-item label="姓名">{{ member.full_name }}</n-descriptions-item>
        <n-descriptions-item label="昵称">{{ member.nickname }}</n-descriptions-item>
        <n-descriptions-item label="性别">{{ member.gender === 'male' ? '男' : '女' }}</n-descriptions-item>
        <n-descriptions-item label="年龄">{{ member.age }}</n-descriptions-item>
        <n-descriptions-item label="手机">{{ member.phone }}</n-descriptions-item>
        <n-descriptions-item label="身份证">{{ member.id_card }}</n-descriptions-item>
        <n-descriptions-item label="会员类型">{{ getMemberTypeText(member.member_type) }}</n-descriptions-item>
        <n-descriptions-item label="会员状态">{{ getStatusText(member.member_status) }}</n-descriptions-item>
        <n-descriptions-item label="活跃积分">{{ member.level_points }}</n-descriptions-item>
        <n-descriptions-item label="等级">{{ member.level_grade }}</n-descriptions-item>
        <n-descriptions-item label="创建时间">{{ member.created_at }}</n-descriptions-item>
      </n-descriptions>

      <n-tabs type="line" style="margin-top: 24px">
        <n-tab-pane name="scores" title="比赛成绩">
          <n-data-table :columns="scoreColumns" :data="scores" :loading="scoresLoading" />
        </n-tab-pane>
        <n-tab-pane name="activities" title="活跃记录">
          <n-data-table :columns="activityColumns" :data="activities" :loading="activitiesLoading" />
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getMemberDetail } from '@/api/modules/member'

const route = useRoute()
const member = ref({})
const scores = ref([])
const activities = ref([])
const scoresLoading = ref(false)
const activitiesLoading = ref(false)

const scoreColumns = [
  { title: '比赛', key: 'competition_name' },
  { title: '项目', key: 'event_item' },
  { title: '成绩', key: 'score_time', render: (row) => `${row.score_time}s` },
  { title: '名次', key: 'rank' },
  { title: '积分', key: 'points' }
]

const activityColumns = [
  { title: '类型', key: 'activity_type_display' },
  { title: '日期', key: 'activity_date' },
  { title: '描述', key: 'description' },
  { title: '积分', key: 'points' }
]

function getMemberTypeText(type) {
  const map = { temp: '临时会员', formal: '正式会员', active: '活跃会员' }
  return map[type] || type
}

function getStatusText(status) {
  const map = { normal: '正常', disabled: '禁用', cancelled: '已注销' }
  return map[status] || status
}

onMounted(async () => {
  try {
    const res = await getMemberDetail(route.params.id)
    member.value = res.data
  } catch (error) {
    console.error(error)
  }
})
</script>
