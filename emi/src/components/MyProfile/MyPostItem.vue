<template>
  <div v-if="product.isActive" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden product pt-6" :data-product-id="product.id" >
    <img :src="product.image" :alt="product.name" class="w-full h-48 object-cover" @click="openProductDetails(product)" />
    <div class="p-4 relative">
      <div v-if="isDeleting" class="absolute right-12 top-5">
        <Loader2 class="h-5 w-5 animate-spin text-red-500"/>
      </div>
      <Trash v-else @click="deletePost" class="h-5 w-5 text-red-500 absolute right-12 top-5 cursor-pointer hover:text-red-600" />

      <div v-if="isLoading" class="absolute right-5 top-5">
        <Loader2 class="h-5 w-5 animate-spin text-gray-500"/>
      </div>
      <template v-else>
        <HeartIcon v-if="!product.liked" @click="like" class="h-5 w-5 text-gray-500 absolute right-5 top-5 cursor-pointer hover:text-gray-600" />
        <HeartHandshakeIcon v-else @click="unlike" class="h-5 w-5 absolute right-5 top-5 text-green-300 cursor-pointer hover:text-green-400"/>
      </template>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ product.name }}</h2>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Price: ${{ product.price.toFixed(2) }}</p>
      <p class="text-sm text-gray-700 dark:text-gray-300 mt-1">
        Stock: <span :class="{'text-red-600 font-bold shadow-xl shadow-white animate-pulse': (product.stockLeft < product.totalStock * 0.1) || (product.stockLeft <= 2 && product.totalStock > 3), 'text-xs': product.stockLeft !== product.totalStock}">{{ product.stockLeft }}</span>
        / {{ product.totalStock }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import { HeartIcon, HeartHandshakeIcon, Trash, Loader2 } from 'lucide-vue-next';
import axios from 'axios';
import { getPostData } from '@/utils';

const isLoading = ref(false);
const isDeleting = ref(false);

const emit = defineEmits(['setProduct', 'viewDetails', 'deletePost']);

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
});

const deletePost = () => {
  isDeleting.value = true;
  emit('deletePost', props.product);
  // Since the actual deletion happens in the parent component,
  // we'll reset the loading state after a short delay
  setTimeout(() => {
    isDeleting.value = false;
  }, 2000);
}

const like = () => {
  isLoading.value = true;
  axios.post(`/api/post/posts/${props.product.id}/like/`)
  .then(
    response => {
      const post = response.data
      const postData = getPostData(post)
      emit('setProduct', postData, props.index)
    }
  )
  .finally(() => {
    isLoading.value = false;
  });
}

const unlike = () => {
  isLoading.value = true;
  axios.post(`/api/post/posts/${props.product.id}/unlike/`)
  .then(
    response => {
      const post = response.data
      const postData = getPostData(post)
      emit('setProduct', postData, props.index)
    }
  )
  .finally(() => {
    isLoading.value = false;
  });
}

const openProductDetails = () => {
  emit('viewDetails', props.product);
};
</script>
