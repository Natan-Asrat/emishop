<script setup>
import { ref, onMounted } from 'vue';
import AuthView from '@/views/AuthView.vue'
import axios from 'axios';
import { RouterView } from 'vue-router';
import { useUserStore } from './stores/user';
import ToastComponent from './components/ToastComponent.vue';
import { WS_BASE_URL } from './config';
import { useToastStore } from './stores/toast';
import { useFeedPostStore } from './stores/feedPost';
import { useFavouritesStore } from './stores/favouritePost';
import { useUserPostsStore } from './stores/userPost';
import { useTransactionsStore } from './stores/transactions';
import { Dialog, DialogPanel } from '@headlessui/vue';
import PopupComponent from './components/App/PopupComponent.vue';

const feedPostStore = useFeedPostStore();
const favouritePostStore = useFavouritesStore();
const userPostStore = useUserPostsStore();
const transactionStore = useTransactionsStore();
const toastStore = useToastStore();
const userStore = useUserStore();
const isAuthenticated = ref(false);
const token = userStore.user.access;
const ws = ref(null)
const isModalVisible = ref(false);
const selectedProduct = ref(null);
const modalContent = ref(null);

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

  <!-- Post Modal -->
  <SelectedProduct
    v-if="selectedProduct"
    :isReserving="isReserving"
    :selectedProduct="selectedProduct"
    @reserveProduct="reserveProduct"
    @closeProductDetails="() => (selectedProduct = null)"
  />

</template>
