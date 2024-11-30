<script setup>
import { ref, onMounted, computed } from 'vue';
import AuthView from '@/views/AuthView.vue'
import axios from 'axios';
import { RouterView } from 'vue-router';
import PWAUpdateHandler from '@/components/PWAUpdateHandler.vue'
import { useUserStore } from './stores/user';
import ToastComponent from './components/ToastComponent.vue';
import { WS_BASE_URL } from './config';
import { useToastStore } from './stores/toast';
import { useFeedPostStore } from './stores/feedPost';
import { useFavouritesStore } from './stores/favouritePost';
import { useUserPostsStore } from './stores/userPost';
import { useTransactionsStore } from './stores/transactions';
import { useNotificationStore } from './stores/notification';
import PopupComponent from './components/App/PopupComponent.vue';
import { useThemeStore } from './stores/theme'
import { Sun, Moon, Monitor } from 'lucide-vue-next'

const notificationStore = useNotificationStore();
const feedPostStore = useFeedPostStore();
const favouritePostStore = useFavouritesStore();
const userPostStore = useUserPostsStore();
const transactionStore = useTransactionsStore();
const toastStore = useToastStore();
const userStore = useUserStore();
const themeStore = useThemeStore()
const isAuthenticated = ref(false);
const token = userStore.user.access;
const ws = ref(null)
const isModalVisible = ref(false);
const modalContent = ref(null);

const currentThemeIcon = computed(() => {
  switch (themeStore.theme) {
    case 'system':
      return { icon: Moon, title: 'Switch to dark mode' }
    case 'dark':
      return { icon: Sun, title: 'Switch to light mode' }
    case 'light':
      return { icon: Monitor, title: 'Switch to system preference' }
  }
})

function toggleTheme() {
  switch (themeStore.theme) {
    case 'system':
      themeStore.updateTheme('dark')
      break
    case 'dark':
      themeStore.updateTheme('light')
      break
    case 'light':
      themeStore.updateTheme('system')
      break
  }
}

const closeModal = () => {
  isModalVisible.value = false;
  modalContent.value = null;
};


onMounted(() => {
  if (token) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    ws.value = new WebSocket(
      `${WS_BASE_URL}/ws/notifications/${userStore.user.id}?token=${token}`
    );
    ws.value.onmessage = async (event) => {
      const message = JSON.parse(event.data)
      console.log('received', message)
      if( message.type === 'notification' ){
        const notification = message.object;
        notificationStore.addNotification(notification);
        toastStore.showToast(
          5000,
          notification.message,
          "bg-green-500 dark:bg-green-500"
        )
        let icon
        if (notification.type === 'popup') {
          console.log("popup")
          isModalVisible.value = true;
          modalContent.value = {
            title: notification.title,
            message: notification.message,
            reservation: notification.reservation,
            post: notification.post,
          };
        }
        if(notification.type === 'reservation'){
          transactionStore.addOrder(notification.reservation);
          transactionStore.addTransaction(notification.reservation);

        }else if(notification.type==='status_update'){

          transactionStore.replaceOrders(notification.reservation);
          transactionStore.replaceTransactions(notification.reservation);
        }
        if(notification.type === 'message'){
          icon = notification.sender.avatar
        }else if(notification.type === 'reservation' || notification.type === 'status_update' || (notification.type === 'popup' && notification.reservation != null)) {
          icon = notification.reservation.post.images[0]
        }else if(notification.type === 'like' || (notification.type === 'popup' && notification.post != null)) {
          icon = notification.post.images[0]
        }else {
          icon = '/logo.png'
        }
          if (Notification.permission === "granted") {
            // Show a notification with the browser's default sound
            new Notification(notification.title, {
              body: notification.message,
              icon,
            });
          } else {
            // If permissions are not granted, request permission
            Notification.requestPermission().then((permission) => {
              if (permission === "granted") {
                new Notification(notification.title, {
                  body: notification.message,
                  icon, // Optional: path to an icon for the notification
                });
              }
            });
          }

          try {
            await markNotificationAsDelivered(notification.id);
          } catch (error) {
            console.error("Failed to mark notification as delivered:", error);
          }
      }else if (message.type === "post") {
        const post = message.object;
        feedPostStore.replacePost(post);
        favouritePostStore.replacePost(post);
        userPostStore.replacePost(post);
        this.postsStore.updateDetailAndCounts(message.object);
      }
    }
    ws.value.onopen = (event) => {
      console.log("WebSocket connection opened:", event);
    };
    ws.value.onerror = (error) => {
      console.log("WebSocket error:", error);
      toastStore.showToast(
        5000,
        "Something went wrong. Please refresh!",
        "bg-red-300 dark:bg-red-300",
      );
    };

    ws.value.onclose = () => {
      console.log("WebSocket connection closed.");
    };
  } else {
    axios.defaults.headers.common["Authorization"] = "";
  }
  isAuthenticated.value = !!token;;
});

const markNotificationAsDelivered = async (notificationId) => {
  if (token) {
    try {
      const response = await axios.patch(
        `/api/notification/notifications/${notificationId}/`,
        { read: true },
      );
      if (response.status === 200) {
        console.log(`Notification ${notificationId} marked as delivered.`);
        console.log(response.data);
      } else {
        console.log(
          `Failed to mark notification ${notificationId} as delivered.`,
        );
      }
    } catch (error) {
      console.error("Error sending PATCH request:", error);
    }
  }
};
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
  <ToastComponent />
  <PopupComponent v-if="isModalVisible" :notification="modalContent" @closeModal="closeModal" />
  <PWAUpdateHandler />
  <button 
    @click="toggleTheme" 
    class="fixed bottom-20 right-4 p-3 rounded-full bg-gray-100 dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300 z-50"
    :title="currentThemeIcon.title"
  >
    <component 
      :is="currentThemeIcon.icon" 
      class="w-6 h-6 text-gray-800 dark:text-gray-200"
    />
  </button>
</template>
