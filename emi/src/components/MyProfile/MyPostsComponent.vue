<template>
  <main ref="mainContent" class="pb-20 min-h-screen bg-gray-200 dark:bg-gray-600">
    <div class="px-4 overflow-y-auto">
      <div class="space-y-6 " :class="{'mt-9': feedPostStore.isSearchExpanded}" >
        <MyPostItem
          v-for="(product, index) in feedPostStore.isSearchExpanded && feedPostStore.searchResults.length > 0 ? feedPostStore.searchResults : feedPostStore.posts"
          :key="product.id"
          :product="product"
          :index="index"
          @setProduct="handleSetProduct"
          @viewDetails="openProductDetails"
        />
      </div>
      <SelectedProduct :isReserving="isReserving" :selectedProduct="selectedProduct" @reserveProduct="reserveProduct" @closeProductDetails="closeProductDetails" />
    </div>
  </main>
</template>
<script setup>
import MyPostItem from '@/components/MyProfile/MyPostItem.vue';
import axios from 'axios';
// import { useRouter } from 'vue-router';
import { onMounted, ref  } from 'vue';
import { useUserPostsStore } from '@/stores/userPost';
// import { useUserStore } from '@/stores/user';
import SelectedProduct from '@/components/Feed/SelectedProduct.vue';

const feedPostStore = useUserPostsStore();
// const userStore = useUserStore();
// const props = defineProps({
//   reachedLast: {
//     type: Boolean,
//     required: true,
//   }
// })
// const emits = defineEmits(['resetLastElement', 'openProductDetails'])
// const showInsufficientCoinsModal = ref(false)

const selectedProduct = ref(null)
const isReserving = ref(false);
// const router = useRouter();
const isLoading = ref(false);
const hasMore = ref(true)
const page = ref(1)


const handleSetProduct = (product, index) => {
  console.log("set", product)
  console.log("prev", feedPostStore.posts[index])
  feedPostStore.changePost(product, index);
}
const openProductDetails = (product) => {
  selectedProduct.value = product
}

const closeProductDetails = () => {
  selectedProduct.value = null
}

const fetchPosts = async () => {
  if (isLoading.value || !hasMore.value) return

  isLoading.value = true
  try {
    let response = await axios.get(`api/account/users/myposts/`)
    const newProducts = response.data.map(post => ({
      id: post.id,
      name: post.title,
      price: parseFloat(post.price),
      image: post.images[0],
      images: post.images, // Assuming single image for now
      stockLeft: post.quantity,
      totalStock: post.initial_quantity,
      liked: post.liked,
      quantity: 1,
      description: post.title, // You might want to add description field in your model
      sellerName: post.created_by.username,
      sellerAvatar: "https://placehold.co/40", // You might want to add avatar in your UserProfile
      postedDate: new Date(post.created_at).toLocaleDateString(),
      embedding: post.embedding
    }))

    feedPostStore.addPosts(newProducts)
    hasMore.value = newProducts.length > 0
    page.value++
  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    isLoading.value = false
  }
}



onMounted(async () => {
  await fetchPosts()
})


// watch(
//   () => props.reachedLast,
//   async (newVal) => {
//     if (newVal) {
//       if(newVal === true){
//         await fetchPosts()
//         emits('resetLastElement')
//       }
//     }
//   }
// );

defineExpose({
  openProductDetails,
});
</script>
