<template>
  <div class="standards-container">
    <n-card title="游泳运动员技术等级标准">
      <template #header-extra>
        <n-space>
          <n-select
            v-model:value="filters.gender"
            :options="genderOptions"
            placeholder="性别"
            style="width: 100px"
            @update:value="loadData"
          />
          <n-select
            v-model:value="filters.pool_length"
            :options="poolOptions"
            placeholder="泳池"
            style="width: 100px"
            @update:value="loadData"
          />
        </n-space>
      </template>

      <n-tabs type="line" animated>
        <n-tab-pane
          v-for="stroke in strokeList"
          :key="stroke.code"
          :tab="stroke.name"
          :name="stroke.code"
        >
          <n-data-table
            :columns="columns"
            :data="getStrokeData(stroke.code)"
            :pagination="false"
            size="small"
          />
        </n-tab-pane>
      </n-tabs>
    </n-card>

    <!-- 成绩对比 -->
    <n-card title="成绩对比" style="margin-top: 16px">
      <n-space vertical>
        <n-grid :cols="4" :x-gap="12">
          <n-gi>
            <n-select v-model:value="compareForm.gender" :options="genderOptions" placeholder="性别" />
          </n-gi>
          <n-gi>
            <n-select v-model:value="compareForm.stroke" :options="strokeOptions" placeholder="泳姿" />
          </n-gi>
          <n-gi>
            <n-select v-model:value="compareForm.distance" :options="distanceOptions" placeholder="距离" />
          </n-gi>
          <n-gi>
            <n-input v-model:value="compareForm.score" placeholder="输入成绩(mm:ss.00)" />
          </n-gi>
        </n-grid>
        <n-button type="primary" @click="compareScore">查询达标</n-button>

        <n-descriptions v-if="compareResult" bordered :column="2">
          <n-descriptions-item label="输入成绩">{{ compareResult.input_formatted }}</n-descriptions-item>
          <n-descriptions-item label="趋势">{{ compareResult.trend }}</n-descriptions-item>
          <n-descriptions-item label="达标等级">
            <n-space>
              <n-tag v-for="level in compareResult.achieved_levels" :key="level.level" type="success">
                {{ level.level_display }}
              </n-tag>
              <n-tag v-if="!compareResult.achieved_levels.length" type="warning">未达标</n-tag>
            </n-space>
          </n-descriptions-item>
          <n-descriptions-item v-if="compareResult.next_level" label="距离下一等级">
            {{ compareResult.next_level.gap }}秒 ({{ compareResult.next_level.level_display }})
          </n-descriptions-item>
        </n-descriptions>
      </n-space>
    </n-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import standardsApi from '@/api'

const loading = ref(false)
const standardsData = ref([])
const compareResult = ref(null)

const filters = reactive({
  gender: 'male',
  pool_length: 50
})

const compareForm = reactive({
  gender: 'male',
  stroke: 'freestyle',
  distance: 100,
  score: ''
})

const genderOptions = [
  { label: '男子', value: 'male' },
  { label: '女子', value: 'female' }
]

const poolOptions = [
  { label: '50米池', value: 50 },
  { label: '25米池', value: 25 }
]

const strokeList = [
  { code: 'freestyle', name: '自由泳' },
  { code: 'backstroke', name: '仰泳' },
  { code: 'breaststroke', name: '蛙泳' },
  { code: 'butterfly', name: '蝶泳' },
  { code: 'medley', name: '混合泳' }
]

const strokeOptions = strokeList.map(s => ({ label: s.name, value: s.code }))

const distanceOptions = [
  { label: '50m', value: 50 },
  { label: '100m', value: 100 },
  { label: '200m', value: 200 },
  { label: '400m', value: 400 },
  { label: '800m', value: 800 },
  { label: '1500m', value: 1500 }
]

const columns = [
  { title: '距离', key: 'distance', width: 80 },
  { title: '国际级健将', key: 'international', width: 120 },
  { title: '运动健将', key: 'national', width: 120 },
  { title: '一级运动员', key: 'level_1', width: 120 },
  { title: '二级运动员', key: 'level_2', width: 120 },
  { title: '三级运动员', key: 'level_3', width: 120 }
]

function getStrokeData(strokeCode) {
  const strokeRecords = standardsData.value.filter(s => s.stroke === strokeCode)
  const distances = [...new Set(strokeRecords.map(r => r.distance))].sort()

  return distances.map(distance => {
    const records = strokeRecords.filter(r => r.distance === distance)
    const row = { distance: `${distance}m` }
    records.forEach(r => {
      row[r.level] = r.formatted_time
    })
    return row
  })
}

async function loadData() {
  try {
    loading.value = true
    const res = await standardsApi.get('/standards/swimming/', {
      params: { gender: filters.gender, pool_length: filters.pool_length }
    })
    if (res.data) {
      standardsData.value = res.data
    }
  } catch (error) {
    console.error('加载标准失败', error)
  } finally {
    loading.value = false
  }
}

async function compareScore() {
  try {
    const score = parseTimeToSeconds(compareForm.score)
    const res = await standardsApi.post('/standards/swimming/compare_score/', {
      gender: compareForm.gender,
      stroke: compareForm.stroke,
      distance: compareForm.distance,
      pool_length: 50,
      score_time: score
    })
    if (res.data) {
      compareResult.value = res.data
    }
  } catch (error) {
    console.error('对比失败', error)
  }
}

function parseTimeToSeconds(timeStr) {
  if (!timeStr) return 0
  const match = timeStr.match(/(\d+):(\d{2})\.(\d{1,2})/)
  if (match) {
    const minutes = parseInt(match[1])
    const seconds = parseInt(match[2])
    const fraction = parseInt(match[3].padEnd(2, '0'))
    return minutes * 60 + seconds + fraction / 100
  }
  return 0
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.standards-container {
  padding: 0;
}
</style>