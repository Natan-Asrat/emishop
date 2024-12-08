<script setup>
import { ref, onMounted, computed, onBeforeMount } from 'vue';
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
import { Sun, Moon, Monitor, Smartphone } from 'lucide-vue-next';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue';

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
const showMobileWarning = ref(false);

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

const checkScreenSize = () => {
  if (window.innerWidth > 768) {
    showMobileWarning.value = true;
  } else {
    showMobileWarning.value = false;
  }
};

onMounted(() => {
  if (token) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    // First verify the token is still valid
    axios.get('/api/account/users/me/')
      .then(() => {
        // Only establish WebSocket connection if token is valid
        ws.value = new WebSocket(
          `${WS_BASE_URL}/ws/notifications/${userStore.user.id}?token=${token}`
        );

        ws.value.onopen = (event) => {
          console.log("WebSocket connection opened:", event);
        };

        ws.value.onerror = (error) => {
          console.error("WebSocket error:", error);
          toastStore.showToast(
            5000,
            "WebSocket connection error. Please refresh!",
            "bg-red-300 dark:bg-red-300",
          );
        };

        ws.value.onclose = () => {
          console.log("WebSocket connection closed.");
          // Try to reconnect after a delay if token is still valid
          setTimeout(() => {
            if (userStore.user.access) {
              console.log("Attempting to reconnect WebSocket...");
              ws.value = new WebSocket(
                `${WS_BASE_URL}/ws/notifications/${userStore.user.id}?token=${userStore.user.access}`
              );
            }
          }, 5000);
        };

        ws.value.onmessage = async (event) => {
          const message = JSON.parse(event.data)
          console.log('received', message)
          if (message.type === 'notification') {
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
            if (notification.type === 'reservation') {
              transactionStore.addOrder(notification.reservation);
              transactionStore.addTransaction(notification.reservation);

            } else if (notification.type === 'status_update') {

              transactionStore.replaceOrders(notification.reservation);
              transactionStore.replaceTransactions(notification.reservation);
            }
            if (notification.type === 'message') {
              icon = notification.sender.avatar
            } else if (notification.type === 'reservation' || notification.type === 'status_update' || (notification.type === 'popup' && notification.reservation != null)) {
              icon = notification.reservation.post.images[0]
            } else if (notification.type === 'like' || (notification.type === 'popup' && notification.post != null)) {
              icon = notification.post.images[0]
            } else {
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
          } else if (message.type === "post") {
            const post = message.object;
            const postData = {
              id: post.id,
              name: post.title,
              price: parseFloat(post.price),
              image: post.images[0],
              images: post.images, // Assuming single image for now
              stockLeft: post.quantity,
              totalStock: post.initial_quantity,
              liked: post.liked,
              quantity: 1,
              isActive: post.is_active,
              description: post.title, // You might want to add description field in your model
              sellerName: post.created_by.username,
              sellerAvatar: "https://placehold.co/40", // You might want to add avatar in your UserProfile
              postedDate: new Date(post.created_at).toLocaleDateString(),
              embedding: post.embedding
            }
            feedPostStore.replacePost(postData);
            favouritePostStore.replacePost(postData);
            userPostStore.replacePost(postData);
            this.postsStore.updateDetailAndCounts(message.object);
          }
        }
      })
      .catch(() => {
        toastStore.showToast(
          5000,
          "Invalid token. Please refresh!",
          "bg-red-300 dark:bg-red-300",
        );
      });
  } else {
    axios.defaults.headers.common["Authorization"] = "";
  }
  isAuthenticated.value = !!token;;
  checkScreenSize();
  window.addEventListener('resize', checkScreenSize);
});

onBeforeMount(() => {
  window.removeEventListener('resize', checkScreenSize);
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
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <Dialog 
      :open="showMobileWarning"
      v-if="showMobileWarning"
      class="relative z-50"
      static
    >
      <div class="fixed inset-0 bg-black/30 backdrop-blur-sm" aria-hidden="true" />
      
      <div class="fixed inset-0 flex w-screen items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-sm rounded-2xl bg-white dark:bg-gray-800 p-6 text-center">
          <div class="flex justify-center mb-4">
            <Smartphone class="w-16 h-16 text-blue-500" />
          </div>
          
          <DialogTitle class="text-2xl font-medium leading-6 text-gray-900 dark:text-white mb-4">
            Please Use Mobile Device
          </DialogTitle>
          
          <div class="mt-4">
            <p class="text-gray-600 dark:text-gray-300">
              Emi Shop is designed for the best experience on mobile devices. 
              Please access the app from your phone or tablet for optimal usage.
            </p>
            
            <div class="mt-6 flex flex-col gap-4">
              <div class="p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                <p class="text-sm text-blue-700 dark:text-blue-300">
                  💡 Tip: Use your mobile device's browser or add to home screen for the best experience!
                </p>
              </div>
            </div>
          </div>
        </DialogPanel>
      </div>
    </Dialog>

    <!-- Rest of your app content -->
    <div :class="{ 'pointer-events-none blur-sm': showMobileWarning }">
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
    </div>
  </div>
</template>
