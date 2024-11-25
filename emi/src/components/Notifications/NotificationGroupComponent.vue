<template>
  <div class="w-full">
    <h3 class="font-sm dark:text-white">{{  notificationGroup.date }}</h3>
    <hr class="mt-1 mb-1"/>
    <div class="space-y-6 mt-6" >
      <NotificationItemComponent v-for="notification in notificationGroup.notifications" :key="notification.id" :notification="notification" />
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
</script>
