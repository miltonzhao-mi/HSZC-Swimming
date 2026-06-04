<template>
  <div class="profile-container">
    <n-card title="会员画像">
      <template #header-extra>
        <n-button @click="refreshData">刷新数据</n-button>
      </template>

      <n-tabs type="line" animated>
        <!-- 基本信息 -->
        <n-tab-pane name="basic" tab="基本信息">
          <n-descriptions bordered :column="2" v-if="basicInfo">
            <n-descriptions-item label="姓名">{{ basicInfo.name }}</n-descriptions-item>
            <n-descriptions-item label="性别">{{ basicInfo.gender === 'male' ? '男' : '女' }}</n-descriptions-item>
            <n-descriptions-item label="年龄">{{ basicInfo.age }}岁</n-descriptions-item>
            <n-descriptions-item label="年龄组">{{ basicInfo.age_group }}</n-descriptions-item>
            <n-descriptions-item label="会员类型">{{ basicInfo.member_type }}</n-descriptions-item>
            <n-descriptions-item label="活跃积分">{{ basicInfo.level_points }}</n-descriptions-item>
          </n-descriptions>
          <n-skeleton v-else type="card" :height="150" />
        </n-tab-pane>

        <!-- 成绩趋势 -->
        <n-tab-pane name="performance" tab="成绩趋势">
          <n-space vertical>
            <n-grid :cols="4" :x-gap="12">
              <n-gi>
                <n-select
                  v-model:value="trendFilters.stroke"
                  :options="strokeOptions"
                  placeholder="选择泳姿"
                  clearable
                  @update:value="loadTrendData"
                />
              </n-gi>
              <n-gi>
                <n-select
                  v-model:value="trendFilters.distance"
                  :options="distanceOptions"
                  placeholder="选择距离"
                  clearable
                  @update:value="loadTrendData"
                />
              </n-gi>
            </n-grid>

            <div ref="chartContainer" style="width: 100%; height: 400px;">
              <n-empty v-if="trendData.length === 0" description="暂无数据" />
            </div>

            <n-data-table
              v-if="trendData.length > 0"
              :columns="trendColumns"
              :data="trendData"
              :pagination="false"
              size="small"
            />
          </n-space>
        </n-tab-pane>

        <!-- 个人最佳 -->
        <n-tab-pane name="bests" tab="个人最佳成绩">
          <n-data-table
            :columns="bestColumns"
            :data="personalBests"
            :loading="loading"
            size="small"
          />
        </n-tab-pane>

        <!-- 活跃度统计 -->
        <n-tab-pane name="participation" tab="活跃度统计">
          <n-grid :cols="4" :x-gap="16" :y-gap="16">
            <n-gi>
              <n-statistic label="年度报名次数">
                <n-number-animation :from="0" :to="participationStats.year_signups" />
              </n-statistic>
            </n-gi>
            <n-gi>
              <n-statistic label="年度有成绩次数">
                <n-number-animation :from="0" :to="participationStats.year_scores" />
              </n-statistic>
            </n-gi>
            <n-gi>
              <n-statistic label="年度参训次数">
                <n-number-animation :from="0" :to="participationStats.year_training" />
              </n-statistic>
            </n-gi>
            <n-gi>
              <n-statistic label="年度积分">
                <n-number-animation :from="0" :to="participationStats.year_points" />
              </n-statistic>
            </n-gi>
          </n-grid>

          <n-divider />

          <h4>历史累计</h4>
          <n-grid :cols="4" :x-gap="16" :y-gap="16">
            <n-gi>
              <n-statistic label="累计报名">{{ participationStats.total_signups }}</n-statistic>
            </n-gi>
            <n-gi>
              <n-statistic label="累计有成绩">{{ participationStats.total_scores }}</n-statistic>
            </n-gi>
            <n-gi>
              <n-statistic label="累计参训">{{ participationStats.total_training }}</n-statistic>
            </n-gi>
            <n-gi>
              <n-statistic label="累计积分">{{ participationStats.total_points }}</n-statistic>
            </n-gi>
          </n-grid>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import profileApi from '@/api/modules/profile'

const route = useRoute()
const loading = ref(false)

// 基本信息
const basicInfo = ref(null)

// 成绩趋势
const trendData = ref([])
const trendFilters = reactive({
  stroke: null,
  distance: null
})
const chartContainer = ref(null)

// 个人最佳
const personalBests = ref([])

// 活跃度统计
const participationStats = reactive({
  year_signups: 0,
  year_scores: 0,
  year_training: 0,
  year_points: 0,
  total_signups: 0,
  total_scores: 0,
  total_training: 0,
  total_points: 0
})

const strokeOptions = [
  { label: '自由泳', value: 'freestyle' },
  { label: '仰泳', value: 'backstroke' },
  { label: '蛙泳', value: 'breaststroke' },
  { label: '蝶泳', value: 'butterfly' },
  { label: '混合泳', value: 'medley' }
]

const distanceOptions = [
  { label: '50m', value: 50 },
  { label: '100m', value: 100 },
  { label: '200m', value: 200 },
  { label: '400m', value: 400 },
  { label: '800m', value: 800 },
  { label: '1500m', value: 1500 }
]

const trendColumns = [
  { title: '日期', key: 'date', width: 120 },
  { title: '比赛', key: 'competition_name', ellipsis: true },
  { title: '成绩', key: 'formatted_time', width: 100 },
  { title: '名次', key: 'rank', width: 80 },
  { title: '变化', key: 'improvement', width: 100 }
]

const bestColumns = [
  { title: '泳姿', key: 'stroke_display', width: 100 },
  { title: '距离', key: 'distance', width: 80 },
  { title: '最佳成绩', key: 'formatted_time', width: 120 },
  { title: '最好名次', key: 'rank', width: 80 },
  { title: '达标等级', key: 'level_display', width: 120 }
]

async function loadBasicInfo() {
  try {
    const memberId = route.params.id || 1
    const res = await profileApi.getSummary(memberId)
    if (res.data) {
      basicInfo.value = res.data.basic_info
      Object.assign(participationStats, {
        ...res.data.participation_stats.current_year,
        ...res.data.participation_stats.all_time
      })
    }
  } catch (error) {
    console.error('加载基本信息失败', error)
  }
}

async function loadTrendData() {
  try {
    const memberId = route.params.id || 1
    const params = {
      member_id: memberId,
      ...trendFilters
    }
    const res = await profileApi.getPerformanceTrend(params)
    if (res.data) {
      trendData.value = res.data.data_points || []
      renderChart(res.data)
    }
  } catch (error) {
    console.error('加载成绩趋势失败', error)
  }
}

async function loadPersonalBests() {
  try {
    loading.value = true
    const memberId = route.params.id || 1
    const res = await profileApi.getPersonalBests(memberId)
    if (res.data && res.data.records) {
      personalBests.value = res.data.records.map(r => ({
        ...r,
        level_display: r.achieved_level ? r.achieved_level.level_display : '-'
      }))
    }
  } catch (error) {
    console.error('加载个人最佳失败', error)
  } finally {
    loading.value = false
  }
}

function renderChart(data) {
  if (!chartContainer.value || !data.data_points || data.data_points.length === 0) return

  nextTick(() => {
    const chart = echarts.init(chartContainer.value)
    const dates = data.data_points.map(d => d.date)
    const times = data.data_points.map(d => d.time)

    chart.setOption({
      title: {
        text: `成绩趋势 - ${data.event}`,
        subtext: `趋势: ${data.trend} | 提升: ${data.improvement_rate}`
      },
      tooltip: {
        formatter: (params) => `${params.name}<br/>成绩: ${params.value}秒`
      },
      xAxis: {
        type: 'category',
        data: dates
      },
      yAxis: {
        type: 'value',
        name: '成绩(秒)',
        inverse: false
      },
      series: [{
        type: 'line',
        data: times,
        smooth: true,
        markPoint: {
          data: [
            { type: 'min', name: '最佳' },
            { type: 'max', name: '最差' }
          ]
        },
        lineStyle: { color: '#c41e3a' },
        itemStyle: { color: '#c41e3a' }
      }],
      grid: {
        left: '10%',
        right: '5%',
        bottom: '15%'
      }
    })
  })
}

function refreshData() {
  loadBasicInfo()
  loadTrendData()
  loadPersonalBests()
}

onMounted(() => {
  loadBasicInfo()
  loadTrendData()
  loadPersonalBests()
})
</script>

<style scoped>
.profile-container {
  padding: 0;
}
</style>