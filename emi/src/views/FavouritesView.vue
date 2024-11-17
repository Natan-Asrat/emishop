<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <h1 class="text-2xl text-gray-900 dark:text-gray-100 font-bold mb-6">Favourites</h1>
    <TabsComponent :current-tab="currentTab" @setCurrentTab="setCurrentTab"/>
    <div class="space-y-4">
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
    </div>
    <div v-if="favouriteStore.posts.length === 0" class="text-center my-auto dark:text-gray-100">
      You don't have any posts here!
    </div>

    <FooterComponent />
</div>

</template>
<script>
import FavouriteItem from '@/components/Favourites/FavouriteItem.vue';
import TabsComponent from '@/components/Favourites/TabsComponent.vue';
import { useFavouritesStore } from '@/stores/favouritePost';
import { useUserStore } from '@/stores/user';
import { useRecommendationStore } from '@/stores/recommendation';
import axios from 'axios';
import FooterComponent from '@/components/FooterComponent.vue';
export default {
  data() {
    return{
      currentTab: 'Favourites',
      isReserving: false,
      requiredCoins: 0,
      showInsufficientCoinsModal: false
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
    TabsComponent,
    FavouriteItem,
    FooterComponent,
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
        this.userStore.user.coins -= req;
        product.stockLeft -= product.quantity;
        this.recommendationStore.updatePostInteraction(product.id, 'reserve', product.quantity);

        this.closeProductDetails();
        this.$router.push('/transactions');

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

  }
}

</script>

