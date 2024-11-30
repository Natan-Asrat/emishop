<template>
  <div class="min-h-screen bg-gray-900 dark:bg-gray-100">
    <NavbarWrapper class="bg-gray-100 dark:bg-gray-900 p-4">
      <h1 class="text-2xl text-gray-900 dark:text-gray-100 font-bold mb-6">Favourites</h1>
    <div v-if="isLoading" class='mb-5 text-center dark:text-gray-100'>Loading...</div>

    </NavbarWrapper>
    <div class="space-y-4 min-h-screen bg-gray-200 dark:bg-gray-600 p-4 mb-12" style="padding-top: 108px">
      <FavouriteItem
        v-for="(product, index) in favouriteStore.posts"
        :key="product.id"
        :product="product"
        :index="index"
        @viewDetails="openProductDetails"
        @reserve="reserveProduct"
        @updateQuantity="favouriteStore.updateProductQuantity"
        @incrementQuantity="favouriteStore.incrementProductQuantity"
        @decrementQuantity="favouriteStore.decrementProductQuantity"
      />
      
    <div v-if="favouriteStore.posts.length == 0" class="text-center dark:text-gray-100 text-gray-900">
      You don't have any liked posts here!
    </div>
    </div>
    <InsufficientCoinsComponent v-if="showInsufficientCoinsModal" :requiredCoins="requiredCoins" :userCoins="userStore.user.coins" @closeInsufficientCoinsModal="showInsufficientCoinsModal = false"  />

    <FooterComponent />
</div>

</template>
<script>
import FavouriteItem from '@/components/Favourites/FavouriteItem.vue';
import { useFavouritesStore } from '@/stores/favouritePost';
import { useUserStore } from '@/stores/user';
import { useRecommendationStore } from '@/stores/recommendation';
import axios from 'axios';
import FooterComponent from '@/components/FooterComponent.vue';
import NavbarWrapper from '@/components/NavbarWrapper.vue';
import InsufficientCoinsComponent from '@/components/InsufficientCoinsComponent.vue';
export default {
  data() {
    return{
      currentTab: 'Favourites',
      isReserving: false,
      requiredCoins: 0,
      showInsufficientCoinsModal: false,
      isLoading: false,
      hasMore: true,
    }
  },
  setup() {
    const favouriteStore = useFavouritesStore();
    const userStore = useUserStore();
    const recommendationStore = useRecommendationStore();

    return {
      favouriteStore,
      userStore,
      recommendationStore
    }

  },
  components: {
    FavouriteItem,
    FooterComponent,
    NavbarWrapper,
    InsufficientCoinsComponent
  },
  methods: {
    setCurrentTab(tab) {
      this.currentTab = tab
    },
    async reserveProduct(product) {
      const req = Math.ceil(product.price * 0.01 * product.quantity);

      if (this.userStore.user.coins < req) {
        this.requiredCoins = req;
        this.showInsufficientCoinsModal = true;
        return;
      }

      try {
        this.isReserving = true;
        await axios.post(`api/reservations/`, {
          post_id: product.id,
          quantity: product.quantity,
        });

        // Update local state
        this.userStore.refreshCoins()
        product.stockLeft -= product.quantity;
        this.recommendationStore.updatePostInteraction(product.id, 'reserve', product.quantity);

        this.closeProductDetails();
        this.$router.push({name: 'transactions'});

      } catch (error) {
        console.error('Error creating reservation:', error);
        if (error.response?.data?.error === 'Insufficient coins') {
          this.requiredCoins = req;
          this.showInsufficientCoinsModal = true;
        } else if (error.response?.data?.error === 'Insufficient stock') {
          alert('This item is out of stock or quantity not available');
        } else {
          alert('Failed to reserve the item. Please try again.');
        }
      } finally {
        this.isReserving = false;
      }
    },
    async fetchPosts() {
      if (this.isLoading || !this.hasMore) return

      this.isLoading = true
      try {
        const response = await axios.get(`api/post/posts/favourites/`)

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
          isActive: post.is_active,
          description: post.title, // You might want to add description field in your model
          sellerName: post.created_by.username,
          sellerAvatar: "https://placehold.co/40", // You might want to add avatar in your UserProfile
          postedDate: new Date(post.created_at).toLocaleDateString(),
          embedding: post.embedding
        }))

        this.favouriteStore.addPosts(newProducts)
        // hasMore.value = newProducts.length > 0
        // page.value++
      } catch (error) {
        console.error('Error fetching posts:', error)
      } finally {
        this.isLoading = false
      }
    }

  },
  async mounted() {
    await this.fetchPosts()
  }
}

</script>

