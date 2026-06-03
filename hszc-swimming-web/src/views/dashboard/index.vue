<template>
  <div class="dashboard">
    <n-grid :cols="4" :x-gap="16" :y-gap="16">
      <n-gi>
        <n-card title="会员总数" size="small">
          <n-statistic :value="stats.total" :value-style="{ color: '#1890ff' }">
            <template #suffix>人</template>
          </n-statistic>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card title="正式会员" size="small">
          <n-statistic :value="stats.formal" :value-style="{ color: '#52c41a' }">
            <template #suffix>人</template>
          </n-statistic>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card title="活跃会员" size="small">
          <n-statistic :value="stats.active" :value-style="{ color: '#faad14' }">
            <template #suffix>人</template>
          </n-statistic>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card title="临时会员" size="small">
          <n-statistic :value="stats.temp" :value-style="{ color: '#722ed1' }">
            <template #suffix>人</template>
          </n-statistic>
        </n-card>
      </n-gi>
    </n-grid>

    <n-grid :cols="2" :x-gap="16" :y-gap="16" style="margin-top: 16px;">
      <n-gi>
        <n-card title="快捷操作">
          <n-space vertical>
            <n-button @click="$router.push('/members')">会员管理</n-button>
            <n-button @click="$router.push('/competitions')">比赛管理</n-button>
            <n-button @click="$router.push('/trainings')">训练管理</n-button>
          </n-space>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card title="最近活动">
          <n-empty description="暂无活动" />
        </n-card>
      </n-gi>
    </n-grid>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMemberStats } from '@/api'

const stats = ref({
  total: 0,
  formal: 0,
  active: 0,
  temp: 0
})

onMounted(async () => {
  try {
    const res = await getMemberStats()
    stats.value = res.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}
</style>
