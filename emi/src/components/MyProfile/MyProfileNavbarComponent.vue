<template>
  <div class="space-y-4 bg-white dark:bg-gray-800 shadow-inner">
    <div v-if="user" class="grid grid-cols-6 p-4">
      <div class="col-span-2 space-y-3">
        <img :src="user.avatar" alt="" class="ml-auto mr-auto w-24 h-24 rounded-full object-cover">
        <div>
          <h1 class="text-xl text-center font-semibold whitespace-nowrap text-gray-900 dark:text-gray-100">{{ user.name }}</h1>
          <h2 class="text-sm text-center whitespace-nowrap text-gray-700 dark:text-gray-300">@{{ user.username }}</h2>
        </div>
        <p class="whitespace-nowrap text-gray-600 dark:text-gray-400"><span class="text-sm">Coins spent </span><span class="block text-md ml-6"><span class="text-sm">{{ user.stats.coins_spent}} </span> / {{ user.stats.coins_bought }}</span> </p>
      </div>

      <div class="col-span-4 space-y-10">
        <div class="grid grid-cols-3 gap-2">
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{user.stats.ads}}</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Ads</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{user.stats.ordered}}</p>
            <p class="text-sm text-gray-600 text-gray-400">Ordered</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ user.stats.delivered }}
            </p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Delivered</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{user.stats.reserved}}</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Reserved</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{user.stats.received}}</p>
            <p class="text-sm text-gray-600 text-gray-400">Received</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ user.stats.canceled }}
            </p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Canceled</p>
          </div>

        </div>
        <div class="flex gap-4">
          <button @click="$router.push({name: 'edit_profile'})" class="text-gray-800  flex-grow rounded-lg h-10 bg-yellow-300">Edit</button>
          <button @click="showLogoutModal = true" class="bg-red-800 text-gray-100 rounded-lg h-10 flex-grow">Logout</button>

        </div>
        <ConfirmLogoutComponent v-if="showLogoutModal" @logout="logout" @closeModal="closeModal" :user="user"/>
      </div>

    </div>
    <div v-if="isLoading" class="p-4">
      <div  class="dark:text-gray-100 text-center">Loading...</div>
    </div>
  </div>
</template>
<script setup>
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ConfirmLogoutComponent from '@/components/MyProfile/ConfirmLogoutComponent.vue';
const userStore = useUserStore()
const toastStore = useToastStore();
const user = ref(null);
const showLogoutModal = ref(false);
const isLoading = ref(false);
const router = useRouter();
const closeModal = () => {
  showLogoutModal.value = false
}
const logout = () => {
  userStore.removeToken();

  router.push({ name: 'home' })
  window.location.reload();

}
onMounted(() => {
  isLoading.value = true;
  axios.get('api/account/users/stats/')
  .then(
    response => {
      console.log("re", response.data)
      user.value = response.data;
      isLoading.value = false;
    }
  )
  .catch(
    error => {
      console.log(error);
      toastStore.showToast(
            5000,
            "Something went wrong. Please try again!",
            "bg-red-300 dark:bg-red-300",
          );
      isLoading.value = false;
    }
  )
});
</script>
