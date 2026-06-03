<template>
  <div class="message-list">
    <n-card title="消息中心">
      <template #header-extra>
        <n-button type="primary" @click="showAddModal = true">发布消息</n-button>
      </template>

      <n-data-table
        :columns="columns"
        :data="data"
        :loading="loading"
        :pagination="pagination"
        :row-key="(row) => row.id"
      />
    </n-card>

    <!-- 发布消息弹窗 -->
    <n-modal v-model:show="showAddModal" preset="card" title="发布消息" style="width: 500px">
      <n-form :model="form" :rules="rules" label-placement="left" label-width="100">
        <n-form-item label="标题" path="title">
          <n-input v-model:value="form.title" placeholder="请输入消息标题" />
        </n-form-item>
        <n-form-item label="内容" path="content">
          <n-input v-model:value="form.content" type="textarea" placeholder="请输入消息内容" />
        </n-form-item>
        <n-form-item label="类型" path="message_type">
          <n-select v-model:value="form.message_type" :options="typeOptions" style="width: 200px" />
        </n-form-item>
        <n-form-item label="立即发布">
          <n-switch v-model:value="form.is_published" />
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
import { getMessageList, createMessage, markMessageRead } from '@/api'
import { NTag, NButton, NSpace } from 'naive-ui'

const loading = ref(false)
const data = ref([])
const showAddModal = ref(false)

const form = reactive({
  title: '',
  content: '',
  message_type: 'system',
  is_published: true
})

const rules = {
  title: { required: true, message: '请输入标题', trigger: 'blur' },
  content: { required: true, message: '请输入内容', trigger: 'blur' },
  message_type: { required: true, message: '请选择类型', trigger: 'change' }
}

const typeOptions = [
  { label: '比赛通知', value: 'competition' },
  { label: '训练通知', value: 'training' },
  { label: '系统通知', value: 'system' },
  { label: '公告', value: 'announcement' }
]

const typeMap = {
  competition: { type: 'info', text: '比赛通知' },
  training: { type: 'success', text: '训练通知' },
  system: { type: 'default', text: '系统通知' },
  announcement: { type: 'warning', text: '公告' }
}

const pagination = reactive({
  page: 1,
  pageSize: 20,
  onChange: (page) => { pagination.page = page; loadData() }
})

const columns = [
  { title: '标题', key: 'title', width: 200 },
  { title: '类型', key: 'message_type', width: 100, render: (row) => {
    const type = typeMap[row.message_type] || { type: 'default', text: row.message_type }
    return h(NTag, { type: type.type, size: 'small' }, { default: () => type.text })
  }},
  { title: '发送人', key: 'sender_name', width: 100 },
  { title: '发布时间', key: 'published_at', width: 180 },
  { title: '操作', key: 'actions', fixed: 'right', width: 150, render: (row) => h(NSpace, { size: 8 }, {
    default: () => [
      h(NButton, { size: 'small', text: true, onClick: () => handleRead(row) }, { default: () => '标记已读' })
    ]
  })}
]

async function loadData() {
  loading.value = true
  try {
    const params = { page: pagination.page, page_size: pagination.pageSize }
    const res = await getMessageList(params)
    data.value = res.data.items || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  try {
    await createMessage(form)
    showAddModal.value = false
    loadData()
  } catch (error) {
    console.error(error)
  }
}

async function handleRead(row) {
  try {
    await markMessageRead(row.id)
    loadData()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => { loadData() })
</script>
