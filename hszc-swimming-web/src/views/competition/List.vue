<template>
  <div class="competition-list">
    <n-card title="比赛管理">
      <template #header-extra>
        <n-button type="primary" @click="showAddModal = true">创建比赛</n-button>
      </template>

      <!-- 筛选 -->
      <n-form :model="searchForm" inline label-placement="left" label-width="80" style="margin-bottom: 16px">
        <n-form-item label="状态">
          <n-select v-model:value="searchForm.status" :options="statusOptions" clearable style="width: 120px" />
        </n-form-item>
        <n-form-item label="关键词">
          <n-input v-model:value="searchForm.keyword" placeholder="比赛名称" clearable style="width: 200px" />
        </n-form-item>
        <n-form-item>
          <n-button type="primary" @click="loadData">搜索</n-button>
        </n-form-item>
      </n-form>

      <!-- 表格 -->
      <n-data-table
        :columns="columns"
        :data="data"
        :loading="loading"
        :pagination="pagination"
        :row-key="(row) => row.id"
      />
    </n-card>

    <!-- 新增/编辑弹窗 -->
    <n-modal v-model:show="showAddModal" preset="card" title="创建比赛" style="width: 600px">
      <n-form :model="form" :rules="rules" label-placement="left" label-width="100">
        <n-form-item label="比赛名称" path="name">
          <n-input v-model:value="form.name" placeholder="请输入比赛名称" />
        </n-form-item>
        <n-form-item label="描述" path="description">
          <n-input v-model:value="form.description" type="textarea" placeholder="请输入描述" />
        </n-form-item>
        <n-form-item label="地点" path="location">
          <n-input v-model:value="form.location" placeholder="请输入比赛地点" />
        </n-form-item>
        <n-grid :cols="2" :x-gap="16">
          <n-gi>
            <n-form-item label="开始日期" path="start_date">
              <n-date-picker v-model:value="form.start_date" type="date" style="width: 100%" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="结束日期" path="end_date">
              <n-date-picker v-model:value="form.end_date" type="date" style="width: 100%" />
            </n-form-item>
          </n-gi>
        </n-grid>
        <n-form-item label="报名截止" path="sign_up_deadline">
          <n-date-picker v-model:value="form.sign_up_deadline" type="datetime" style="width: 100%" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button type="primary" @click="handleSubmit">提交</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCompetitionList, createCompetition } from '@/api/modules/competition'
import { NTag, NButton, NSpace } from 'naive-ui'

const router = useRouter()
const loading = ref(false)
const data = ref([])
const showAddModal = ref(false)

const searchForm = reactive({
  status: null,
  keyword: ''
})

const form = reactive({
  name: '',
  description: '',
  location: '',
  start_date: null,
  end_date: null,
  sign_up_deadline: null
})

const rules = {
  name: { required: true, message: '请输入比赛名称', trigger: 'blur' },
  location: { required: true, message: '请输入比赛地点', trigger: 'blur' },
  start_date: { required: true, message: '请选择开始日期', trigger: 'change' },
  end_date: { required: true, message: '请选择结束日期', trigger: 'change' },
  sign_up_deadline: { required: true, message: '请选择报名截止时间', trigger: 'change' }
}

const statusOptions = [
  { label: '筹备中', value: 'preparing' },
  { label: '报名中', value: 'registration' },
  { label: '进行中', value: 'ongoing' },
  { label: '已结束', value: 'finished' }
]

const statusMap = {
  preparing: { type: 'default', text: '筹备中' },
  registration: { type: 'info', text: '报名中' },
  ongoing: { type: 'success', text: '进行中' },
  finished: { type: 'warning', text: '已结束' }
}

const pagination = reactive({
  page: 1,
  pageSize: 20,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100],
  onChange: (page) => { pagination.page = page; loadData() },
  onUpdatePageSize: (pageSize) => { pagination.pageSize = pageSize; loadData() }
})

const columns = [
  { title: 'ID', key: 'id', width: 80 },
  { title: '比赛名称', key: 'name', width: 200 },
  { title: '地点', key: 'location', width: 150 },
  { title: '日期', key: 'start_date', width: 120, render: (row) => row.start_date },
  { title: '报名人数', key: 'signup_count', width: 100 },
  { title: '状态', key: 'status', width: 100, render: (row) => {
    const status = statusMap[row.status] || { type: 'default', text: row.status }
    return h(NTag, { type: status.type, size: 'small' }, { default: () => status.text })
  }},
  { title: '操作', key: 'actions', fixed: 'right', width: 200, render: (row) => h(NSpace, { size: 8 }, {
    default: () => [
      h(NButton, { size: 'small', text: true, onClick: () => router.push(`/competitions/${row.id}`) }, { default: () => '详情' }),
      h(NButton, { size: 'small', text: true, type: 'primary', onClick: () => handleSignUp(row) }, { default: () => '报名' })
    ]
  })}
]

async function loadData() {
  loading.value = true
  try {
    const params = { page: pagination.page, page_size: pagination.pageSize, ...searchForm }
    const res = await getCompetitionList(params)
    data.value = res.data.items
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  try {
    const data = { ...form }
    if (form.start_date) data.start_date = new Date(form.start_date).toISOString().split('T')[0]
    if (form.end_date) data.end_date = new Date(form.end_date).toISOString().split('T')[0]
    if (form.sign_up_deadline) data.sign_up_deadline = new Date(form.sign_up_deadline).toISOString()
    await createCompetition(data)