<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <img src="@/assets/logo.jpg" alt="logo" class="login-logo" />
        <h2>北京红衫众成游泳俱乐部</h2>
        <p>管理信息系统</p>
      </div>
      <n-form
        ref="formRef"
        :model="form"
        :rules="rules"
        size="large"
      >
        <n-form-item path="username" label="用户名">
          <n-input v-model:value="form.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item path="password" label="密码">
          <n-input
            v-model:value="form.password"
            type="password"
            placeholder="请输入密码"
            show-password-on="click"
          />
        </n-form-item>
        <n-form-item>
          <n-button
            type="primary"
            :loading="loading"
            :disabled="loading"
            block
            @click="handleLogin"
          >
            登录
          </n-button>
        </n-form-item>
      </n-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMessage } from 'naive-ui'
import { h } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const message = useMessage()
const formRef = ref(null)
const loading = ref(false)

const form = ref({
  username: '',
  password: ''
})

const rules = {
  username: { required: true, message: '请输入用户名', trigger: 'blur' },
  password: { required: true, message: '请输入密码', trigger: 'blur' }
}

async function handleLogin() {
  try {
    await formRef.value.validate()
    loading.value = true
    await authStore.login(form.value.username, form.value.password)
    message.success('登录成功')
    router.push('/')
  } catch (error) {
    if (error.message) {
      message.error(error.message)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h2 {
  font-size: 24px;
  color: #c41e3a;
  margin: 0 0 8px 0;
}

.login-logo {
  height: 60px;
  margin-bottom: 16px;
}

.login-header p {
  color: #666;
  margin: 0;
}
</style>
