<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <NavbarWrapper class="bg-gray-100 dark:bg-gray-900 p-4">
      <h1 class="text-2xl text-gray-900 dark:text-gray-100 font-bold mb-6">Notifications</h1>
    <TabsComponent :currentTab="currentTab" @setCurrentTab="setCurrentTab"/>
    </NavbarWrapper>
    <div class="space-y-4 mt-6 mb-12" style="margin-top: 213px">
      <NotificationGroupComponent @setPopupContent="setPopupContent" @setIsPopupVisible="setIsPopupVisible" @openProductDetails="openProductDetails" v-for="notificationGroup in notificationStore.groupedNotifications" :key="notificationGroup" :notificationGroup="notificationGroup" />
    </div>
    <div class="text-center dark:text-gray-100" v-if="notificationStore.notifications.length === 0">
      You don't have any notifications.
    </div>
    <FooterComponent />
    <SpinnerComponent v-if="isLoading"/>
    <PopupComponent v-if="isPopupVisible" :notification="popupContent" @closeModal="closeModal" />
    <SelectedProduct :isReserving="isReserving" :selectedProduct="selectedProduct" @reserveProduct="reserveProduct" @closeProductDetails="closeProductDetails" />
    <InsufficientCoinsComponent v-if="showInsufficientCoinsModal" :requiredCoins="requiredCoins" :userCoins="userStore.user.coins" @closeInsufficientCoinsModal="showInsufficientCoinsModal = false" />
  </div>
</template>
<script>
import FooterComponent from "@/components/FooterComponent.vue";
import TabsComponent from "@/components/Notifications/TabsComponent.vue";
import { useNotificationStore } from "@/stores/notification";
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import NavbarWrapper from "@/components/NavbarWrapper.vue";
import NotificationGroupComponent from "@/components/Notifications/NotificationGroupComponent.vue";
import { useUserStore } from "@/stores/user";
import SelectedProduct from "@/components/Feed/SelectedProduct.vue";
import PopupComponent from "@/components/App/PopupComponent.vue";
import InsufficientCoinsComponent from "@/components/InsufficientCoinsComponent.vue"
import SpinnerComponent from "@/components/SpinnerComponent.vue";
export default {
  name: "NotificationView",
  components: {
    FooterComponent,
    TabsComponent,
    NavbarWrapper,
    NotificationGroupComponent,
    SelectedProduct,
    PopupComponent,
    SpinnerComponent,
    InsufficientCoinsComponent
  },
  data() {
    return {
      currentTab: 'All',
      isReserving: false,
      selectedProduct: null,
      requiredCoins: 0,
      showInsufficientCoinsModal: false,
      isPopupVisible: false,
      popupContent: null,
      isLoading: false,
      page: 1,
      hasMore: true,
    }
  },
  setup() {
    const notificationStore = useNotificationStore()
    const toastStore = useToastStore()
    const userStore = useUserStore();
    return {
      notificationStore,
      toastStore,
      userStore
    }
  },
  methods: {
    fetchNotifications() {
      const url = this.currentTab === 'All' 
        ? `api/notification/notifications/?page=${this.page}`
        : `/api/notification/notifications/?type=${this.currentTab.toLowerCase()}&page=${this.page}`;

      this.isLoading = true;
      axios.get(url)
        .then(response => {
          this.isLoading = false;
          
          this.hasMore = response.data.next !== null;
          
          if (this.page === 1) {
            this.notificationStore.setNotifications(response.data.results)
          } else {
            this.notificationStore.addNotifications(response.data.results)
          }
        })
        .catch(error => {
          console.error(error)
          this.isLoading = false;
          this.toastStore.showToast(
            5000,
            "Something went wrong. Please refresh!",
            "bg-red-300 dark:bg-red-300"
          )
        })
    },
    closeModal() {
      this.isPopupVisible = false;
      this.popupContent = null;
    },
    setPopupContent(content) {
      this.popupContent = content
    },
    setIsPopupVisible(visibility){
      this.isPopupVisible = visibility;
    },
    openProductDetails (product) {
      this.selectedProduct = product
    },
    async reserveProduct(product) {
      const req = Math.ceil(product.price * 0.01 * product.quantity);

      if (this.userStore.user.coins < req) {
        this.requiredCoins = req;
        this.showInsufficientCoinsModal = true;
        return;
      }

      try {
        this.isReserving = true;
        await axios.post(`api/transaction/reservations/`, {
          post_id: product.id,
          quantity: product.quantity,
        });

        this.userStore.refreshCoins()
        product.stockLeft -= product.quantity;

        this.closeProductDetails();
        this.$router.push({name: 'transactions'});

      } catch (error) {
        console.error('Error creating reservation:', error);
        if (error.response?.data?.error === 'Insufficient coins') {
          this.requiredCoins = req;
          this.showInsufficientCoinsModal = true;
        } else if (error.response?.data?.error === 'Insufficient stock') {
          alert('This item is out of stock or quantity not available');
        } else {
          alert('Failed to reserve the item. Please try again.');
        }
      } finally {
        this.isReserving = false;
      }
    },
    closeProductDetails() {
      this.selectedProduct = null
    },
    setCurrentTab(tab) {
      this.currentTab = tab
      this.page = 1
      this.hasMore = true
    },
    handleScroll() {
      if (this.isLoading || !this.hasMore) return;
      
      const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      
      if (bottomOfWindow) {
        this.page += 1;
        this.fetchNotifications();
      }
    },
  },
  mounted() {
    this.fetchNotifications()
    window.addEventListener('scroll', this.handleScroll)
  },
  unmounted() {
    window.removeEventListener('scroll', this.handleScroll) 
  },
  watch: {
    currentTab: {
      handler(newTab){
        this.fetchNotifications()
      },
      immediate: true,
    }
  }
}
</script>
