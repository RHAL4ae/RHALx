<template>
  <div class="policy-manager">
    <h2>إدارة السياسات</h2>
    <form @submit.prevent="addRule">
      <input v-model="rule.device_id" placeholder="معرف الجهاز" required />
      <input v-model="rule.action" placeholder="الإجراء (on/off)" required />
      <button type="submit">إضافة قاعدة</button>
    </form>
    <div v-if="addedId">تمت إضافة القاعدة برقم: {{ addedId }}</div>
    <div class="rules-list">
      <h3>قائمة القواعد</h3>
      <ul>
        <li v-for="(r, id) in rules" :key="id">
          <span>جهاز: {{ r.device_id }} | إجراء: {{ r.action }}</span>
          <button @click="deleteRule(id)">حذف</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const rule = ref({ device_id: '', action: '' })
const addedId = ref('')
const rules = ref<Record<string, any>>({})

async function addRule() {
  addedId.value = ''
  const res = await fetch('/smart/rule', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(rule.value)
  })
  const data = await res.json()
  if (data.rule_id) {
    addedId.value = data.rule_id
    await fetchRules()
  }
}
async function fetchRules() {
  // نفترض أن معرف القاعدة يبدأ من 1
  const temp: Record<string, any> = {}
  for (let i = 1; i < 20; i++) {
    const res = await fetch(`/smart/rule/${i}`)
    if (res.ok) {
      temp[i] = await res.json()
    }
  }
  rules.value = temp
}
async function deleteRule(id: string) {
  await fetch(`/smart/rule/${id}`, { method: 'DELETE' })
  await fetchRules()
}
onMounted(fetchRules)
</script>

<style scoped>
.policy-manager {
  font-family: 'Cairo', Arial, sans-serif;
  background: #e3f2fd;
  border-radius: 12px;
  padding: 2rem;
  max-width: 500px;
  margin: 2rem auto;
  box-shadow: 0 2px 8px #0001;
}
form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
input {
  font-family: inherit;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #90caf9;
}
button {
  font-family: inherit;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  background: #1976d2;
  color: #fff;
  cursor: pointer;
}
button:hover {
  background: #0d47a1;
}
.rules-list {
  margin-top: 1.5rem;
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
  border: 1px solid #90caf9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>