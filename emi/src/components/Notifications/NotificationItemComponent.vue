<template>
  <div @click="click" class="rounded-md p-4 w-full bg-gray-200 dark:bg-gray-800 rounded-md hover:bg-gray-500 dark:hover:bg-gray-500 focus:bg-gray-500 focus:dark:bg-gray-500">
    <h4 :class="[textColor]" class="font-xs mb-3">{{ notification.title }}</h4>
    <div class="flex">
      <img v-if="image && isMessage" :src="image" alt="" class="ml-4 w-10 h-10 object-cover rounded-full ">
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
import { useRouter } from 'vue-router';
const router = useRouter();
const props = defineProps({
  notification: {
    type: Object,
    required: true,
  }
})
const emit = defineEmits(['openProductDetails', 'setIsPopupVisible', 'setPopupContent'])
const isMessage = props.notification.type === 'message';
const isPost = props.notification.type === 'like' || (props.notification.type === 'popup' && props.notification.post != null);
const isReservation = props.notification.type === 'reservation' || props.notification.type === 'status_update' || (props.notification.type === 'popup' && props.notification.reservation != null);
const isPopup = props.notification.type === 'popup';
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
const click = () => {
  if(isReservation){
    router.push({name: 'transactions'});
  }else if(isMessage){
    router.push({
      name: 'chat',
      query: {
        username: props.notification.sender.username,
        itemId: props.notification?.reservation?.id
      }
    });
  }else if(isPost) {

    const product = {
      id: props.notification?.post.id,
      name: props.notification?.post.title,
      price: parseFloat(props.notification?.post.price),
      image: props.notification?.post.images[0],
      images: props.notification?.post.images, // Assuming single image for now
      stockLeft: props.notification?.post.quantity,
      totalStock: props.notification?.post.initial_quantity,
      liked: props.notification?.post.liked,
      quantity: 1,
      description: props.notification?.post.title, // You might want to add description field in your model
      sellerName: props.notification?.post.created_by.username,
      sellerAvatar: "https://placehold.co/40", // You might want to add avatar in your UserProfile
      postedDate: new Date(props.notification?.post.created_at).toLocaleDateString(),
      embedding: props.notification?.post.embedding
    }
    emit('openProductDetails', product)
  }else if(isPopup){
    emit('setIsPopupVisible', true)
    emit('setPopupContent', {
      title: props.notification.title,
      message: props.notification.message,
      reservation: props.notification.reservation,
      post: props.notification.post,
    })
  }
}
const textColor = getStatusColor()
const image = getImage()

</script>
