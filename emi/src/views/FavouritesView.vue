<template>
  <div class="min-h-screen bg-gray-900 dark:bg-gray-100">
    <NavbarWrapper class="bg-gray-100 dark:bg-gray-900 p-4">
      <h1 class="text-2xl text-gray-900 dark:text-gray-100 font-bold mb-6">Favourites</h1>
    <div v-if="favouriteStore.isLoading" class='mb-5 text-center dark:text-gray-100'>Loading...</div>

    </NavbarWrapper>
    <div class="space-y-4 min-h-screen bg-gray-200 dark:bg-gray-600 p-4 mb-12" style="padding-top: 108px">
      <FavouriteItem
        v-for="(product, index) in favouriteStore.posts"
        :key="product.id"
        :product="product"
        :index="index"
        :isReserving="isReserving"
        @viewDetails="openProductDetails"
        @reserve="reserveProduct"
        @updateQuantity="favouriteStore.updateProductQuantity"
        @incrementQuantity="favouriteStore.incrementProductQuantity"
        @decrementQuantity="favouriteStore.decrementProductQuantity"
      />
      
    <div v-if="favouriteStore.posts.length == 0" class="text-center dark:text-gray-100 text-gray-900">
      You don't have any liked posts here!
    </div>
    <SpinnerComponent v-if="favouriteStore.isLoading"/>

    </div>
    <InsufficientCoinsComponent v-if="showInsufficientCoinsModal" :requiredCoins="requiredCoins" :userCoins="userStore.user.coins" @closeInsufficientCoinsModal="showInsufficientCoinsModal = false"  />

    <FooterComponent />
</div>

</template>
<script>
import SpinnerComponent from '@/components/SpinnerComponent.vue';
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
    InsufficientCoinsComponent,
    SpinnerComponent
  },
  methods: {
    setCurrentTab(tab) {
      this.currentTab = tab
    },
    async reserveProduct (product) {
      const req = Math.ceil(product.price * 0.01 * product.quantity);

      if (this.userStore.user.coins < req) {
        this.requiredCoins = req;
        this.showInsufficientCoinsModal = true;
        return;
      }

      try {
        this.isReserving = true;
        await axios.post(`api/transaction/reservations/`, {
          post_id: product.id,
          quantity: product.quantity,
        });

        // Update local state
        this.userStore.refreshCoins()
        product.stockLeft -= product.quantity;
        this.recommendationStore.updatePostInteraction(product.id, 'reserve', product.quantity);

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
    async fetchFavorites() {
      if (this.favouriteStore.isLoading || !this.favouriteStore.hasMore) return;

      this.favouriteStore.isLoading = true;
      
      try {
        const response = await axios.get(`api/post/posts/favourites/?page=${this.favouriteStore.page}&page_size=10`);
        
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
        }));

        // Update store
        if (this.favouriteStore.page === 1) {
          this.favouriteStore.setPosts(newProducts);
        } else {
          this.favouriteStore.addPosts(newProducts);
        }

        // Update pagination
        this.favouriteStore.hasMore = response.data.next !== null;
        if (this.favouriteStore.hasMore) {
          this.favouriteStore.incrementPage();
        }

      } catch (error) {
        console.error('Error fetching favorites:', error);
      } finally {
        this.favouriteStore.isLoading = false;
      }
    },
    handleScroll() {
      if (this.favouriteStore.isLoading || !this.favouriteStore.hasMore) return;
      
      const bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      
      if (bottomOfWindow) {
        this.fetchFavorites();
      }
    }
  },
  mounted() {
    this.favouriteStore.resetPagination();
    this.fetchFavorites();
    window.addEventListener('scroll', this.handleScroll);
  },
  unmounted() {
    window.removeEventListener('scroll', this.handleScroll);
  }
}

</script>
