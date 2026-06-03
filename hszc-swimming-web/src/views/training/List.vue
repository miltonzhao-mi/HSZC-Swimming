<template>
  <div class="training-list">
    <n-card title="训练管理">
      <template #header-extra>
        <n-button type="primary" @click="showAddModal = true">发布训练</n-button>
      </template>

      <n-data-table
        :columns="columns"
        :data="data"
        :loading="loading"
        :pagination="pagination"
        :row-key="(row) => row.id"
      />
    </n-card>

    <!-- 发布训练弹窗 -->
    <n-modal v-model:show="showAddModal" preset="card" title="发布训练通知" style="width: 600px">
      <n-form :model="form" :rules="rules" label-placement="left" label-width="100">
        <n-form-item label="标题" path="title">
          <n-input v-model:value="form.title" placeholder="请输入训练标题" />
        </n-form-item>
        <n-form-item label="训练内容" path="content">
          <n-input v-model:value="form.content" type="textarea" placeholder="请输入训练内容" />
        </n-form-item>
        <n-form-item label="训练地点" path="location">
          <n-input v-model:value="form.location" placeholder="请输入训练地点" />
        </n-form-item>
        <n-grid :cols="2" :x-gap="16">
          <n-gi>
            <n-form-item label="训练日期" path="train_date">
              <n-date-picker v-model:value="form.train_date" type="date" style="width: 100%" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="教练" path="coach">
              <n-input v-model:value="form.coach" placeholder="请输入教练姓名" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="开始时间" path="start_time">
              <n-time-picker v-model:value="form.start_time" format="HH:mm" style="width: 100%" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="结束时间" path="end_time">
              <n-time-picker v-model:value="form.end_time" format="HH:mm" style="width: 100%" />
            </n-form-item>
          </n-gi>
        </n-grid>
        <n-form-item label="报名截止" path="signup_deadline">
          <n-date-picker v-model:value="form.signup_deadline" type="datetime" style="width: 100%" />
        </n-form-item>
        <n-form-item label="通知方式" path="notice_type">
          <n-radio-group v-model:value="form.notice_type">
            <n-radio value="push">小程序推送</n-radio>
            <n-radio value="notice">公告通知</n-radio>
          </n-radio-group>
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button type="primary" @click="handleSubmit">发布</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getTrainingNoticeList, createTrainingNotice } from '@/api/modules/training'
import { NTag, NButton, NSpace } from 'naive-ui'

const loading = ref(false)
const data = ref([])
const showAddModal = ref(false)

const form = reactive({
  title: '',
  content: '',
  location: '',
  train_date: null,
  start_time: null,
  end_time: null,
  coach: '',
  signup_deadline: null,
  notice_type: 'push'
})

const rules = {
  title: { required: true, message: '请输入标题', trigger: 'blur' },
  location: { required: true, message: '请输入地点', trigger: 'blur' },
  train_date: { required: true, message: '请选择日期', trigger: 'change' },
  coach: { required: true, message: '请输入教练', trigger: 'blur' }
}

const pagination = reactive({
  page: 1,
  pageSize: 20,
  onChange: (page) => { pagination.page = page; loadData() }
})

const columns = [
  { title: 'ID', key: 'id', width: 80 },
  { title: '标题', key: 'title', width: 200 },
  { title: '训练日期', key: 'train_date', width: 120 },
  { title: '时间', key: 'start_time', width: 100, render: (row) => `${row.start_time}-${row.end_time}` },
  { title: '地点', key: 'location', width: 150 },
  { title: '教练', key: 'coach', width: 100 },
  { title: '报名人数', key: 'signup_count', width: 100 },
  { title: '状态', key: 'status', width: 100, render: (row) => {
    const map = { draft: '草稿', published: '已发布' }
    return map[row.status] || row.status
  }},
  { title: '操作', key: 'actions', fixed: 'right', width: 150, render: (row) => h(NSpace, { size: 8 }, {
    default: () => [
      h(NButton, { size: 'small', text: true, onClick: () => handleViewSignups(row) }, { default: () => '报名详情' })
    ]
  }})
]

async function loadData() {
  loading.value = true
  try {
    const params = { page: pagination.page, page_size: pagination.pageSize }
    const res = await getTrainingNoticeList(params)
    data.value = res.data.items || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  try {
    const data = { ...form }
    if (form.train_date) data.train_date = new Date(form.train_date).toISOString().split('T')[0]
    if (form.start_time) data.start_time = new Date(form.start_time).toTimeString().slice(0, 5)
    if (form.end_time) data.end_time = new Date(form.end_time).toTimeString().slice(0, 5)
    if (form.signup_deadline) data.signup_deadline = new Date(form.signup_deadline).toISOString()
    await createTrainingNotice(data)
    showAddModal.value = false
    loadData()
  } catch (error) {
    console.error(error)
  }
}

function handleViewSignups(row) {
  // TODO: 跳转查看报名详情
}

onMounted(() => { loadData() })
</script>
