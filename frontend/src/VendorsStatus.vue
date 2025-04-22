<template>
  <div class="vendors-status">
    <h2>حالة المزودين</h2>
    <div v-for="vendor in vendors" :key="vendor" class="vendor-box">
      <span>{{ vendorNames[vendor] }}</span>
      <button @click="fetchStatus(vendor)">تحديث</button>
      <span v-if="status[vendor]">الحالة: {{ status[vendor] }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const vendors = ['nokia', 'huawei', 'tuya']
const vendorNames: Record<string, string> = { nokia: 'نوكيا', huawei: 'هواوي', tuya: 'تويا' }
const status = ref<Record<string, string>>({})

async function fetchStatus(vendor: string) {
  status.value[vendor] = '...'
  const res = await fetch(`/vendor/${vendor}/status`)
  const data = await res.json()
  status.value[vendor] = data.status || data.error || JSON.stringify(data)
}
</script>

<style scoped>
.vendors-status {
  font-family: 'Cairo', Arial, sans-serif;
  background: #f1f8e9;
  border-radius: 12px;
  padding: 2rem;
  max-width: 500px;
  margin: 2rem auto;
  box-shadow: 0 2px 8px #0001;
}
.vendor-box {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  background: #fff;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #aed581;
}
button {
  font-family: inherit;
  padding: 0.3rem 1rem;
  border-radius: 6px;
  border: none;
  background: #388e3c;
  color: #fff;
  cursor: pointer;
}
button:hover {
  background: #1b5e20;
}
</style>