<template>
  <div class="tuya-control">
    <h2>التحكم في أجهزة Tuya</h2>
    <div>
      <input v-model="deviceId" placeholder="معرف الجهاز" />
      <button @click="turnOn">تشغيل</button>
      <button @click="turnOff">إيقاف</button>
    </div>
    <div v-if="result">
      <p>النتيجة: {{ result }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const deviceId = ref('')
const result = ref('')

async function turnOn() {
  result.value = ''
  const res = await fetch(`/vendor/tuya/device/${deviceId.value}/on`, { method: 'POST' })
  result.value = await res.text()
}
async function turnOff() {
  result.value = ''
  const res = await fetch(`/vendor/tuya/device/${deviceId.value}/off`, { method: 'POST' })
  result.value = await res.text()
}
</script>

<style scoped>
.tuya-control {
  font-family: 'Cairo', Arial, sans-serif;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  margin: 2rem auto;
  box-shadow: 0 2px 8px #0001;
}
input {
  font-family: inherit;
  padding: 0.5rem;
  margin-left: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  font-family: inherit;
  margin: 0.5rem 0.5rem 0 0;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  background: #007bff;
  color: #fff;
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
</style>