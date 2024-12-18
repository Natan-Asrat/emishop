<template>
  <div ref="recentlyViewed" class="bg-white dark:bg-gray-800 shadow-inner overflow-hidden">
    <div class="py-4">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3 px-4">Recently Viewed</h2>
      <div class="flex overflow-x-auto space-x-4 pb-4 scrollbar-hide px-4">
        <div v-for="product in recentProducts" :key="product.id" class="flex-shrink-0" >
          <div @click="open(product)" class="w-20 h-20 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
            <img loading="lazy" :src="product.images[0]" :alt="product.name" class="w-full h-full object-cover" />
          </div>
          <p class="mt-2 text-xs text-center text-gray-600 dark:text-gray-400">{{ product.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
defineProps({
  recentProducts: {
    type: Array,
    required: true
  }
})
const emit = defineEmits(['open'])
const open = (post) => {
  const product = {
      id: post.id,
      name: post.title,
      price: parseFloat(post.price),
      image: post.images[0],
      images: post.images,
      stockLeft: post.quantity,
      totalStock: post.initial_quantity,
      liked: post.liked,
      quantity: 1,
      description: post.title, 
      sellerName: post.created_by.username,
      sellerAvatar: post.created_by.avatar,
      postedDate: new Date(post.created_at).toLocaleDateString(),
      embedding: post.embedding
    }
    emit('open', product)
}
</script>
