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
          @deletePost="deletePost"
        />
      </div>
      
    <div class="text-center dark:text-gray-100" v-if="!feedPostStore.posts || feedPostStore.posts.length === 0">
      You don't have any posts yet.
    </div>
    <SpinnerComponent v-if="feedPostStore.isLoading"/>
      <SelectedProduct :isDeleting="isDeleting" :selectedProduct="selectedProduct" @deletePost="deletePost" @closeProductDetails="closeProductDetails" />
    </div>
  </main>
  
</template>
<script setup>
import MyPostItem from '@/components/MyProfile/MyPostItem.vue';
import axios from 'axios';
// import { useRouter } from 'vue-router';
import { onMounted, ref, onUnmounted  } from 'vue';
import { useUserPostsStore } from '@/stores/userPost';
import { useToastStore } from '@/stores/toast';
import SpinnerComponent from '@/components/SpinnerComponent.vue';
// import { useUserStore } from '@/stores/user';
import SelectedProduct from '@/components/MyProfile/SelectedProduct.vue';
const toastStore = useToastStore();
const deletePost = (post) => {
  axios.delete(`api/post/posts/${post.id}/deactivate/`)
  .then(
    response => {
      window.location.reload()
    }
  )
  .catch(
    error => {
      console.error(error)
      toastStore.showToast(
              5000,
              "Something went wrong. Please refresh!)",
              "bg-red-300 dark:bg-red-300"
            )
    }
  )

}

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
const isDeleting = ref(false);
// const router = useRouter();
const isLoading = ref(false);
const hasMore = ref(true)
const page = ref(1)


const handleSetProduct = (product, index) => {
  feedPostStore.changePost(product, index);
}
const openProductDetails = (product) => {
  selectedProduct.value = product
}

const closeProductDetails = () => {
  selectedProduct.value = null
}

const fetchPosts = async () => {
  if (feedPostStore.isLoading || !feedPostStore.hasMore) return

  feedPostStore.isLoading = true
  try {
    let response = await axios.get(`api/account/users/myposts/`, {
      params: {
        page: feedPostStore.page,
        page_size: 10  // Match backend default page size
      }
    })
    
    const newProducts = response.data.results.map(post => ({
      id: post.id,
      name: post.title,
      price: parseFloat(post.price),
      image: post.images[0],
      images: post.images,
      stockLeft: post.quantity,
      totalStock: post.initial_quantity,
      liked: post.liked,
      quantity: 1,
      currency: post.currency,
      tags: post.tags,
      created_by: post.created_by,
      created_at: post.created_at,
      isActive: post.is_active
    }))

    if (feedPostStore.page === 1) {
      feedPostStore.setPosts(newProducts)
    } else {
      feedPostStore.addPosts(newProducts)
    }

    // Update hasMore based on the 'next' field in the response
    feedPostStore.hasMore = response.data.next !== null
    if (feedPostStore.hasMore) {
      feedPostStore.incrementPage()
    }
  } catch (error) {
    console.error('Error fetching posts:', error)
    toastStore.showToast(
      5000,
      "Error loading posts. Please try again!",
      "bg-red-300 dark:bg-red-300"
    )
  } finally {
    feedPostStore.isLoading = false
  }
}

const handleScroll = () => {
  const mainContent = document.documentElement
  const scrolledToBottom = mainContent.scrollTop + mainContent.clientHeight >= mainContent.scrollHeight - 100
  if (scrolledToBottom) {
    fetchPosts()
  }
}

onMounted(async () => {
  feedPostStore.resetPagination()
  await fetchPosts()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

defineExpose({
  openProductDetails,
});
</script>
