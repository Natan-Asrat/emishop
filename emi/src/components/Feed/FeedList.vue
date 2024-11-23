<template>
  <main ref="mainContent" class="pb-20 bg-gray-200 dark:bg-gray-600">
    <div class="px-4 overflow-y-auto" style="padding-top: 300px">
      <div class="space-y-6 " :class="{'mt-9': feedPostStore.isSearchExpanded}" >
        <FeedItem
          v-for="(product, index) in feedPostStore.isSearchExpanded && feedPostStore.searchResults.length > 0 ? feedPostStore.searchResults : feedPostStore.posts"
          :key="product.id"
          :product="product"
          :index="index"
          @setProduct="handleSetProduct"
          @viewDetails="openProductDetails"
          @reserve="reserveProduct"
          @updateQuantity="feedPostStore.updateProductQuantity"
          @incrementQuantity="feedPostStore.incrementQuantity"
          @decrementQuantity="feedPostStore.decrementQuantity"
        />
      </div>
      <SelectedProduct :isReserving="isReserving" :selectedProduct="selectedProduct" @reserveProduct="reserveProduct" @closeProductDetails="closeProductDetails" />
    </div>
  </main>
</template>
<script setup>
import FeedItem from '@/components/Feed/FeedItem.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted, nextTick, watch, ref, defineEmits  } from 'vue';
import { useFeedPostStore } from '@/stores/feedPost';
import { useRecommendationStore } from '@/stores/recommendation';
import { useUserStore } from '@/stores/user';
import SelectedProduct from '@/components/Feed/SelectedProduct.vue';

const recommendationStore = useRecommendationStore();
const feedPostStore = useFeedPostStore();
const userStore = useUserStore();
const props = defineProps({
  reachedLast: {
    type: Boolean,
    required: true,
  }
})
const emits = defineEmits(['resetLastElement'])
const showInsufficientCoinsModal = ref(false)

const selectedProduct = ref(null)
const isReserving = ref(false);
const router = useRouter();
const isLoading = ref(false);
const hasMore = ref(true)
const page = ref(1)
const userEmbedding = ref(new Array(recommendationStore.EMBEDDING_SIZE).fill(0))


const handleSetProduct = (product, index) => {
  console.log("set", product)
  console.log("prev", feedPostStore.posts[index])
  feedPostStore.changePost(product, index);
}
const requiredCoins = ref(0)
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
    router.push('/transactions');

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
  if (isLoading.value || !hasMore.value) return

  isLoading.value = true
  try {
    const mainEmbeddings = JSON.parse(localStorage.getItem('mainEmbeddings') || '[]')
    let response

    if (mainEmbeddings !== null && mainEmbeddings.length >= 60) {
      // If we have enough interaction data, send user embedding
      // response = await axios.post(`${API_URL}/posts/feed/`, {
      //   user_embedding: userEmbedding.value
      // })
      response = await axios.post(`api/post/posts/feed/`, {user_embedding: userEmbedding.value})
    } else {
      // Otherwise, get diverse results
      response = await axios.get(`api/post/posts/feed/`)
    }
    console.log("res", response.data)
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
    for(const product of newProducts){
      recommendationStore.updatePostInteraction(product.id, 'view')

    }

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
  recommendationStore.loadUserData();
  await fetchPosts()

  nextTick(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
          const productId = entry.target.dataset.productId; // Ensure your elements have a data-product-id attribute
          if (entry.isIntersecting) {
              // Element is in the viewport
              recommendationStore.updateVisibility(productId, true);
          } else {
              // Element has left the viewport
              recommendationStore.updateVisibility(productId, false);
          }
      });
  });

  // Assuming you have elements with the class 'product' and data-product-id
  const productElements = document.querySelectorAll('.product');
  productElements.forEach((element) => observer.observe(element));
  })
})

onUnmounted(() => {
  recommendationStore.saveUserData()
})

watch(
  () => props.reachedLast,
  async (newVal) => {
    if (newVal) {
      if(newVal === true){
        const topPosts =recommendationStore.calculateTopInteractedPosts()
        recommendationStore.setTopPosts(topPosts)
        recommendationStore.saveToTemporaryStore(feedPostStore.posts)
        recommendationStore.updateMainListAndGenerateEmbedding()
        await fetchPosts()
        emits('resetLastElement')
      }
    }
  }
);
watch([recommendationStore.postInteractions, recommendationStore.interactionTimes, recommendationStore.userEmbedding, recommendationStore.tempEmbeddings], recommendationStore.saveUserData, { deep: true })

</script>
