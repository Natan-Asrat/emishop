<template>
  <div class="w-full">
    <h3 class="font-sm dark:text-white">{{  notificationGroup.date }}</h3>
    <hr class="mt-1 mb-1"/>
    <div class="space-y-6 mt-6" >
      <NotificationItemComponent @setPopupContent="setPopupContent" @setIsPopupVisible="setIsPopupVisible" @openProductDetails="openProductDetails" v-for="notification in notificationGroup.notifications" :key="notification.id" :notification="notification" />
    </div>
  </div>
</template>
<script setup>
import NotificationItemComponent from './NotificationItemComponent.vue';

defineProps({
  notificationGroup: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['openProductDetails'])
const openProductDetails = (product) => {
  emit('openProductDetails', product)
}
const setIsPopupVisible = (visibility) => {
  emit('setIsPopupVisible', visibility)
}
const setPopupContent = (content) => {
  emit('setPopupContent', content)
}
</script>
