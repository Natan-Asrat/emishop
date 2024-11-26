<template>

  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <NavbarWrapper class="bg-gray-100 dark:bg-gray-900 p-4">
      <h1 class="text-2xl text-gray-900 dark:text-gray-100 font-bold mb-6">Notifications</h1>
    <div v-if="isLoading" class='mb-5 text-center dark:text-gray-100'>Loading...</div>
    <TabsComponent :currentTab="currentTab" @setCurrentTab="setCurrentTab"/>

    </NavbarWrapper>
    <div class="space-y-4 mt-6 mb-12" style="margin-top: 213px">
      <NotificationGroupComponent @setPopupContent="setPopupContent" @setIsPopupVisible="setIsPopupVisible" @openProductDetails="openProductDetails" v-for="notificationGroup in notificationStore.groupedNotifications" :key="notificationGroup" :notificationGroup="notificationGroup" />

    </div>
    <div class="text-center dark:text-gray-100" v-if="notificationStore.notifications.length === 0">
      You don't have any notifications.
    </div>
    <FooterComponent />
    <PopupComponent v-if="isPopupVisible" :notification="popupContent" @closeModal="closeModal" />
    <SelectedProduct :isReserving="isReserving" :selectedProduct="selectedProduct" @reserveProduct="reserveProduct" @closeProductDetails="closeProductDetails" />
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
export default {
  name: "NotificationView",
  components: {
    FooterComponent,
    TabsComponent,
    NavbarWrapper,
    NotificationGroupComponent,
    SelectedProduct,
    PopupComponent
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
      console.log("fetching", this.currentTab)
      if(this.currentTab === 'All'){
        axios.get('api/notification/notifications/')
        .then(
          response => {
            console.log("resp all", response.data)
            this.notificationStore.setNotifications(response.data)
          }
        )
        .catch(
          error => {
            console.log("error", error)
            this.toastStore.showToast(
              5000,
              "Something went wrong. Please refresh!",
              "bg-red-300 dark:bg-red-300"
            )
          }
        )
      }else {

        axios.get(`/api/notification/notifications/?type=${this.currentTab.toLowerCase()}`)
        .then(
          response => {
            console.log("resp", response.data)

            this.notificationStore.setNotifications(response.data)
          }
        )
        .catch(
          error => {
            console.log("error", error)

            this.toastStore.showToast(
              5000,
              "Something went wrong. Please refresh!",
              "bg-red-300 dark:bg-red-300"
            )
          }
        )

      }
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

        // Update local state
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
    }

  },
  mounted() {
    this.fetchNotifications()
  },
  watch: {
    currentTab: {
      handler(newTab){
        console.log("tab", newTab)
        this.fetchNotifications()
      },
      immediate: true,
    }
  }

}
</script>
