<template>
  <div v-if="product.isActive" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden product pt-6" :data-product-id="product.id" >
    <img :src="product.image" :alt="product.name" class="w-full h-48 object-cover" @click="openProductDetails(product)" />
    <div class="p-4 relative">
      <Trash @click="deletePost" class="h-5 w-5 text-red-500 ml-auto right-12 top-5 absolute" />

      <HeartIcon v-if="!product.liked" @click="like" class="h-5 w-5 text-red-500 ml-auto right-5 top-5 absolute" />
      <HeartHandshakeIcon v-else @click="unlike" class="h-5 w-5 ml-auto right-5 top-5 absolute text-green-300"/>
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
import { defineProps, defineEmits } from 'vue';
import { HeartIcon, HeartHandshakeIcon, Trash } from 'lucide-vue-next';
import axios from 'axios';
import { getPostData } from '@/utils';
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
  emit('deletePost', props.product)
}

const like = () => {
  axios.post(`api/post/posts/${props.product.id}/like/`)
  .then(
    response => {
      const post = response.data
      const postData = getPostData(post)
      emit('setProduct', postData, props.index)
    }
  )

}
const unlike = () => {
  axios.post(`api/post/posts/${props.product.id}/unlike/`)
  .then(
    response => {
      const post = response.data
      const postData = getPostData(post)
      emit('setProduct', postData, props.index)
    }
  )

}


const openProductDetails = () => {
  emit('viewDetails', props.product);
};
</script>
