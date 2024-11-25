<template>
  <div class="rounded-md p-4 w-full bg-gray-200 dark:bg-gray-800 rounded-md hover:bg-gray-500 dark:hover:bg-gray-500 focus:bg-gray-500 focus:dark:bg-gray-500">
    <h4 :class="[textColor]" class="font-xs mb-3">{{ notification.title }}</h4>
    <div class="flex">
      <img v-if="image && isMessage" :src="image" alt="" class="ml-4 w-10 h-full object-cover rounded-full ">
      <p v-if="isMessage" class="flex-grow dark:text-gray-200 pl-4" style="font-size: 20px;">
        <span v-if="notification?.sender?.username">{{ notification.sender.username }}</span>
        <span v-else>Unknown</span>
      </p>
      <p v-if="isMessage" class="font-xs dark:text-gray-200 pl-4 ml-2" style="font-size: 16px">
        "{{ notification.message }}"
      </p>

      <p v-if="!isMessage" class="flex-grow font-xs dark:text-gray-200 pl-4">
        {{ notification.message }}
      </p>

      <img v-if="image && !isMessage" :src="image" alt="" class="w-20 h-full object-cover rounded-md ">
    </div>
    <div class="relative h-6 mt-2">
      <span class="font-xs dark:text-gray-400 right-0 absolute">{{  notification.created_at_formatted }} ago</span>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  notification: {
    type: Object,
    required: true,
  }
})
const isMessage = props.notification.type === 'message';
const isPost = props.notification.type === 'like' || (props.notification.type === 'popup' && props.notification.post != null);
const isReservation = props.notification.type === 'reservation' || props.notification.type === 'status_update' || (props.notification.type === 'popup' && props.notification.reservation != null);

const getImage = () => {
  let image;
  if(isMessage){
    image = props.notification?.sender?.avatar
  }else if(isReservation) {
    image = props.notification?.reservation?.post?.images[0]
  }else if(isPost) {
    image = props.notification?.post?.images[0]
  }
  if(image != null) {
    return image
  }
  return null
}
const getStatusColor = () => {
  if(isReservation){
    if (props.notification.reservation.status === 'completed') return 'text-green-600 dark:text-green-400';
    if (props.notification.reservation.status === 'cancelled') return 'text-red-600 dark:text-red-400';
    if (props.notification.reservation.status === 'reported') return 'text-yellow-600 dark:text-yellow-400';
  }else if(isMessage){
    return 'text-blue-600 dark:text-blue-400';
  }else if(isPost) {
    return 'text-purple-600 dark:text-purple-400';
  }
  return 'dark:text-white'
};
const textColor = getStatusColor()
const image = getImage()

</script>
