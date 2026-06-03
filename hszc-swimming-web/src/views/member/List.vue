<template>
  <div class="member-list">
    <n-card title="会员管理">
      <template #header-extra>
        <n-space>
          <n-button type="primary" @click="showAddModal = true">新增会员</n-button>
          <n-button @click="showImportModal = true">批量导入</n-button>
        </n-space>
      </template>

      <!-- 搜索筛选 -->
      <n-form :model="searchForm" inline label-placement="left" label-width="80">
        <n-form-item label="会员类型">
          <n-select v-model:value="searchForm.member_type" :options="memberTypeOptions" clearable style="width: 120px" />
        </n-form-item>
        <n-form-item label="会员状态">
          <n-select v-model:value="searchForm.member_status" :options="memberStatusOptions" clearable style="width: 120px" />
        </n-form-item>
        <n-form-item label="关键词">
          <n-input v-model:value="searchForm.keyword" placeholder="姓名/手机/身份证" clearable style="width: 200px" />
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
    <n-modal v-model:show="showAddModal" preset="card" title="会员信息" style="width: 800px">
      <n-form :model="form" :rules="rules" label-placement="left" label-width="100">
        <n-grid :cols="2" :x-gap="16">
          <n-gi>
            <n-form-item label="姓" path="surname">
              <n-input v-model:value="form.surname" placeholder="请输入姓" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="名" path="given_name">
              <n-input v-model:value="form.given_name" placeholder="请输入名" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="昵称" path="nickname">
              <n-input v-model:value="form.nickname" placeholder="请输入昵称" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="身份证号" path="id_card">
              <n-input v-model:value="form.id_card" placeholder="请输入身份证号" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="性别" path="gender">
              <n-radio-group v-model:value="form.gender">
                <n-radio value="male">男</n-radio>
                <n-radio value="female">女</n-radio>
              </n-radio-group>
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="出生日期" path="birth_date">
              <n-date-picker v-model:value="form.birth_date" type="date" style="width: 100%" />
            </n-form-item>
          </n-gi>
          <n-gi>
            <n-form-item label="联系电话" path="phone">
              <n-input v-model:value="form.phone" placeholder="请输入手机号" />
            </n-form-item>
          </n-gi>
        </n-grid>
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
import { getMemberList, createMember, approveMember, upgradeMember, cancelMember } from '@/api/modules/member'
import { NTag, NButton, NSpace, NPopconfirm } from 'naive-ui'

const router = useRouter()
const loading = ref(false)
const data = ref([])
const showAddModal = ref(false)
const showImportModal = ref(false)

const searchForm = reactive({
  member_type: null,
  member_status: null,
  keyword: ''
})

const form = reactive({
  surname: '',
  given_name: '',
  nickname: '',
  id_card: '',
  gender: 'male',
  birth_date: null,
  phone: ''
})

const rules = {
  surname: { required: true, message: '请输入姓', trigger: 'blur' },
  given_name: { required: true, message: '请输入名', trigger: 'blur' },
  id_card: { required: true, message: '请输入身份证号', trigger: 'blur' },
  gender: { required: true, message: '请选择性别', trigger: 'change' },
  birth_date: { required: true, message: '请选择出生日期', trigger: 'change' },
  phone: { required: true, message: '请输入联系电话', trigger: 'blur' }
}

const memberTypeOptions = [
  { label: '临时会员', value: 'temp' },
  { label: '正式会员', value: 'formal' },
  { label: '活跃会员', value: 'active' }
]

const memberStatusOptions = [
  { label: '正常', value: 'normal' },
  { label: '禁用', value: 'disabled' },
  { label: '已注销', value: 'cancelled' }
]

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
  { title: '姓名', key: 'full_name', width: 120 },
  { title: '昵称', key: 'nickname', width: 120 },
  { title: '性别', key: 'gender', width: 80, render: (row) => row.gender === 'male' ? '男' : '女' },
  { title: '年龄', key: 'age', width: 80 },
  { title: '手机', key: 'phone', width: 130 },
  { title: '类型', key: 'member_type', width: 100, render: (row) => {
    const map = { temp: '临时', formal: '正式', active: '活跃' }
    return map[row.member_type] || row.member_type
  }},
  { title: '状态', key: 'member_status', width: 100, render: (row) => {
    const map = { normal: '正常', disabled: '禁用', cancelled: '已注销' }
    return map[row.member_status] || row.member_status
  }},
  { title: '积分', key: 'level_points', width: 80 },
  { title: '操作', key: 'actions', fixed: 'right', width: 200, render: (row) => {
    const actions = []
    actions.push(h(NButton, { size: 'small', text: true, onClick: () => router.push(`/members/${row.id}`) }, { default: () => '详情' }))
    if (row.member_type === 'temp' && row.member_status === 'normal') {
      actions.push(h(NButton, { size: 'small', text: true, type: 'success', onClick: () => handleApprove(row) }, { default: () => '审批' }))
    }
    if (row.member_type === 'temp') {
      actions.push(h(NButton, { size: 'small', text: true, type: 'warning', onClick: () => handleUpgrade(row) }, { default: () => '升级' }))
    }
    if (row.member_status === 'normal') {
      actions.push(h(NPopconfirm, { onPositiveClick: () => handleCancel(row) }, {
        trigger: () => h(NButton, { size: 'small', text: true, type: 'error' }, { default: () => '注销' }),
        default: () => '确定注销该会员?'
      }))
    }
    return h(NSpace, { size: 8 }, { default: () => actions })
  }}
]

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    const res = await getMemberList(params)
    data.value = res.data.items
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async