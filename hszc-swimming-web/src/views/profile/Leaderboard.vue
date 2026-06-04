<template>
  <div class="leaderboard-container">
    <n-card title="活跃度排行榜">
      <template #header-extra>
        <n-space>
          <n-select
            v-model:value="filters.type"
            :options="typeOptions"
            style="width: 120px"
            @update:value="loadData"
          />
          <n-select
            v-model:value="filters.gender"
            :options="genderOptions"
            placeholder="性别"
            clearable
            style="width: 100px"
            @update:value="loadData"
          />
          <n-select
            v-model:value="filters.age_group"
            :options="ageGroupOptions"
            placeholder="年龄组"
            clearable
            style="width: 100px"
            @update:value="loadData"
          />
        </n-space>
      </template>

      <n-data-table
        :columns="columns"
        :data="rankings"
        :loading="loading"
        :pagination="pagination"
      />
    </n-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import profileApi from '@/api/modules/profile'

const loading = ref(false)
const rankings = ref([])
const filters = reactive({
  type: 'annual',
  gender: null,
  age_group: null
})

const typeOptions = [
  { label: '年度排行', value: 'annual' },
  { label: '历史排行', value: 'all_time' }
]

const genderOptions = [
  { label: '全部', value: null },
  { label: '男', value: 'male' },
  { label: '女', value: 'female' }
]

const ageGroupOptions = [
  { label: '全部', value: null },
  { label: '20岁以下', value: '0-19' },
  { label: '20-29岁', value: '20-29' },
  { label: '30-39岁', value: '30-39' },
  { label: '40-49岁', value: '40-49' },
  { label: '50岁以上', value: '50-100' }
]

const columns = [
  { title: '排名', key: 'rank', width: 80 },
  { title: '姓名', key: 'member_name', width: 120 },
  { title: '性别', key: 'gender', width: 80, render: (row) => row.gender === 'male' ? '男' : '女' },
  { title: '年龄组', key: 'age_group', width: 100 },
  { title: '年度积分', key: 'year_points', width: 100 },
  { title: '累计积分', key: 'level_points', width: 100 },
  { title: '年度有成绩', key: 'total_scores', width: 120 },
  { title: '年度报名', key: 'total_signups', width: 100 }
]

const pagination = reactive({
  page: 1,
  pageSize: 20
})

async function loadData() {
  try {
    loading.value = true
    const res = await profileApi.getLeaderboard(filters)
    if (res.data && res.data.rankings) {
      rankings.value = res.data.rankings
    }
  } catch (error) {
    console.error('加载排行榜失败', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.leaderboard-container {
  padding: 0;
}
</style>