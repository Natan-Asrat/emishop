<template>
  <main ref="mainContent" class="pb-20 min-h-screen bg-gray-200 dark:bg-gray-600">
    <div class="px-4 overflow-y-auto">
      <div class="space-y-6 " :class="{'mt-9': feedPostStore.isSearchExpanded}" >
        <FeedItem
          v-for="(product, index) in feedPostStore.isSearchExpanded && feedPostStore.searchResults.length > 0 ? feedPostStore.searchResults : feedPostStore.posts"
          :key="product.id"
          :product="product"
          :index="index"
          :isReserving="isReserving"
          @setProduct="handleSetProduct"
          @viewDetails="openProductDetails"
          @reserve="reserveProduct"
          @updateQuantity="feedPostStore.updateProductQuantity"
          @incrementQuantity="feedPostStore.incrementQuantity"
          @decrementQuantity="feedPostStore.decrementQuantity"
        />
      </div>
      <SpinnerComponent v-if="feedPostStore.isLoading"/>

      <div class="text-center text-gray-900 dark:text-gray-100 mt-4" v-if="!feedPostStore.isLoading && feedPostStore.posts.length === 0">
        <p class="text-lg">There are no posts yet. Be the first to post!</p>
      </div>
      <InsufficientCoinsComponent v-if="showInsufficientCoinsModal" :requiredCoins="requiredCoins" :userCoins="userStore.user.coins" @closeInsufficientCoinsModal="showInsufficientCoinsModal = false"  />
      <SelectedProduct :isReserving="isReserving" :selectedProduct="selectedProduct" @reserveProduct="reserveProduct" @closeProductDetails="closeProductDetails" />
    </div>
  </main>
</template>
<script setup>
import FeedItem from '@/components/Feed/FeedItem.vue';
import InsufficientCoinsComponent from '@/components/InsufficientCoinsComponent.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted, nextTick, watch, ref, defineEmits  } from 'vue';
import { useFeedPostStore } from '@/stores/feedPost';
import { useRecommendationStore } from '@/stores/recommendation';
import { useUserStore } from '@/stores/user';
import SelectedProduct from '@/components/Feed/SelectedProduct.vue';
import SpinnerComponent from '@/components/SpinnerComponent.vue';
const recommendationStore = useRecommendationStore();
const feedPostStore = useFeedPostStore();
const userStore = useUserStore();
const props = defineProps({
  reachedLast: {
    type: Boolean,
    required: true,
  }
})
const emits = defineEmits(['resetLastElement', 'openProductDetails', 'searchMore'])
const showInsufficientCoinsModal = ref(false)

const selectedProduct = ref(null)
const isReserving = ref(false);
const router = useRouter();
const requiredCoins = ref(0)

const handleSetProduct = (product, index) => {
  feedPostStore.changePost(product, index);
}

const openProductDetails = (product) => {
  selectedProduct.value = product
  recommendationStore.updatePostInteraction(product.id, 'detailView')
  const startTime = Date.now()
  product.startViewTime = startTime
}

const closeProductDetails = () => {
  if (selectedProduct.value) {
    const endTime = Date.now()
    const timeSpent = (endTime - selectedProduct.value.startViewTime) / 1000 // Convert to seconds
    recommendationStore.updateInteractionTime(selectedProduct.value.id, timeSpent)
  }
  selectedProduct.value = null
}
const reserveProduct = async (product) => {
  const req = Math.ceil(product.price * 0.01 * product.quantity);

  if (userStore.user.coins < req) {
    requiredCoins.value = req;
    showInsufficientCoinsModal.value = true;
    return;
  }

  try {
    isReserving.value = true;
    await axios.post(`api/transaction/reservations/`, {
      post_id: product.id,
      quantity: product.quantity,
    });

    // Update local state
    userStore.refreshCoins()
    product.stockLeft -= product.quantity;
    recommendationStore.updatePostInteraction(product.id, 'reserve', product.quantity);

    closeProductDetails();
    router.push({name: 'transactions'});

  } catch (error) {
    console.error('Error creating reservation:', error);
    if (error.response?.data?.error === 'Insufficient coins') {
      requiredCoins.value = req;
      showInsufficientCoinsModal.value = true;
    } else if (error.response?.data?.error === 'Insufficient stock') {
      alert('This item is out of stock or quantity not available');
    } else {
      alert('Failed to reserve the item. Please try again.');
    }
  } finally {
    isReserving.value = false;
  }
};

const fetchPosts = async () => {
  if (feedPostStore.isSearchExpanded && feedPostStore.searchResults.length > 0) {
    emits('searchMore')
  } 
  if (feedPostStore.isLoading || !feedPostStore.hasMore) return

  feedPostStore.isLoading = true
  try {
    const mainEmbeddings = JSON.parse(localStorage.getItem('mainEmbeddings') || '[]')
    let response

    if (mainEmbeddings !== null && mainEmbeddings.length >= 60) {
      // If we have enough interaction data, send user embedding in batches of 10
      response = await axios.post(`api/post/posts/feed/?page=${feedPostStore.page}`, {
        user_embedding: recommendationStore.userEmbedding,
        page_size: 10
      })
    } else {
      // Otherwise, get diverse results in batches of 10
      response = await axios.get(`api/post/posts/feed/?page=${feedPostStore.page}&page_size=10`)
    }
    
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
      isActive: post.is_active,
      description: post.title,
      sellerName: post.created_by.username,
      sellerAvatar: post.created_by.avatar,
      postedDate: new Date(post.created_at).toLocaleDateString(),
      embedding: post.embedding
    }))

    // Update store with new products
    if (feedPostStore.page === 1) {
      feedPostStore.setPosts(newProducts)
    } else {
      feedPostStore.addPosts(newProducts)
    }

    // Update pagination
    feedPostStore.hasMore = response.data.next !== null
    if (feedPostStore.hasMore) {
      feedPostStore.incrementPage()
    }

    // Track interactions
    for(const product of newProducts){
      recommendationStore.updatePostInteraction(product.id, 'view')
    }

  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    feedPostStore.isLoading = false
  }
}

// Handle scroll
const handleScroll = () => {
  if (feedPostStore.isLoading || !feedPostStore.hasMore) return;
  
  const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
  
  if (bottomOfWindow) {
    fetchPosts();
  }
}

// Lifecycle hooks
onMounted(() => {
  feedPostStore.resetPagination()
  fetchPosts()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

watch(
  () => props.reachedLast,
  async (newVal) => {
    if (newVal) {
      if(newVal === true){
        const topPosts =recommendationStore.calculateTopInteractedPosts()
        recommendationStore.setTopPosts(topPosts)
        recommendationStore.saveTopPostsToRecentlyViewed(topPosts)
        recommendationStore.saveToTemporaryStore(feedPostStore.posts)
        recommendationStore.updateMainListAndGenerateEmbedding()
        await fetchPosts()
        emits('resetLastElement')
      }
    }
  }
);
watch([recommendationStore.postInteractions, recommendationStore.interactionTimes, recommendationStore.userEmbedding, recommendationStore.tempEmbeddings], recommendationStore.saveUserData, { deep: true })

defineExpose({
  openProductDetails,
});
</script>
