<template>
  <n-config-provider :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <router-view />
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import zhCN from 'naive-ui/es/locale/zh-CN.mjs'
import dateZhCN from 'naive-ui/es/date-locale/zh-CN.mjs'
</script>
