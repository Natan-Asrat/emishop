<template>

  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <NavbarWrapper class="bg-gray-100 dark:bg-gray-900 p-4">
      <h1 class="text-2xl text-gray-900 dark:text-gray-100 font-bold mb-6">Notifications</h1>
    <div v-if="isLoading" class='mb-5 text-center dark:text-gray-100'>Loading...</div>
    <TabsComponent :currentTab="currentTab" @setCurrentTab="setCurrentTab"/>

    </NavbarWrapper>
    <div class="space-y-4 mt-6 mb-12" style="margin-top: 213px">
      <NotificationGroupComponent v-for="notificationGroup in notificationStore.groupedNotifications" :key="notificationGroup" :notificationGroup="notificationGroup" />

    </div>
    <div class="text-center dark:text-gray-100" v-if="notificationStore.notifications.length === 0">
      You don't have any notifications.
    </div>
    <FooterComponent />
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
export default {
  name: "NotificationView",
  components: {
    FooterComponent,
    TabsComponent,
    NavbarWrapper,
    NotificationGroupComponent
  },
  data() {
    return {
      currentTab: 'All'
    }
  },
  setup() {
    const notificationStore = useNotificationStore()
    const toastStore = useToastStore()
    return {
      notificationStore,
      toastStore
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
            this.toastStore.showToast(
              5000,
              "Something went wrong. Please refresh!",
              "bg-red-300 dark:bg-red-300"
            )
          }
        )

      }
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
        this.fetchNotifications()
      },
      immediate: true,
    }
  }

}
</script>
