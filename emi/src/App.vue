<script setup>
import { ref, onMounted } from 'vue';
import AuthView from '@/views/AuthView.vue'
import axios from 'axios';
import { RouterView } from 'vue-router';
import { useUserStore } from './stores/user';
const userStore = useUserStore();
const isAuthenticated = ref(false);
const token = userStore.user.access;
onMounted(() => {
  console.log("token", token)
  console.log("user", userStore.user)

  if (token) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    axios.defaults.headers.common["Authorization"] = "";
  }
  isAuthenticated.value = !!token;;
});

const onAuthSuccess = () => {
  isAuthenticated.value = true;
};

const logout = () => {
  // clearSession();
  userStore.clearToken();
  isAuthenticated.value = false;
};

// Expose logout method to be used by child components
defineExpose({ logout });
</script>

<template>

  <RouterView v-if="isAuthenticated" />
  <AuthView v-else @auth-success="onAuthSuccess" />
</template>
