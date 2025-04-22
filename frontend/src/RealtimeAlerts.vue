<template>
  <div class="alerts-box">
    <h2>التنبيهات اللحظية</h2>
    <ul>
      <li v-for="(alert, idx) in alerts" :key="idx">{{ alert }}</li>
    </ul>
    <div v-if="!connected" class="disconnected">غير متصل بالخادم</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
const alerts = ref<string[]>([])
const connected = ref(false)
let ws: WebSocket | null = null

onMounted(() => {
  ws = new WebSocket(`ws://${window.location.host}/alerts/ws`)
  ws.onopen = () => { connected.value = true }
  ws.onmessage = (event) => { alerts.value.unshift(event.data) }
  ws.onclose = () => { connected.value = false }
})
onUnmounted(() => { if (ws) ws.close() })
</script>

<style scoped>
.alerts-box {
  font-family: 'Cairo', Arial, sans-serif;
  background: #fff3cd;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  margin: 2rem auto;
  box-shadow: 0 2px 8px #0001;
  border: 1px solid #ffeeba;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  background: #fff;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #ffeeba;
}
.disconnected {
  color: #b71c1c;
  margin-top: 1rem;
}
</style>