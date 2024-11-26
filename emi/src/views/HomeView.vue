<template>
  <NavbarWrapper @reachedLastElement="reachedLastElement">

    <Navbar />
    <RecentlyViewed @open="handleRecentlyViewedOpen" v-if="recentProducts && recentProducts.length > 0"  :recentProducts="recentProducts" />
  </NavbarWrapper>
  <FeedList   ref="feedList"
  :style="{paddingTop: (recentProducts && recentProducts.length > 0 ) ? '300px' : '100px'}" :reachedLast="reachedLast" @resetLastElement="resetLastElement" />
  <FooterComponent />
</template>
<script>
import Navbar from '@/components/Navbar.vue';
import FeedList from '@/components/Feed/FeedList.vue';
import RecentlyViewed from '@/components/RecentlyViewed.vue';
import NavbarWrapper from '@/components/NavbarWrapper.vue';
import FooterComponent from '@/components/FooterComponent.vue';
import axios from 'axios';
export default {
  name: 'HomeView',
  components: {
    Navbar,
    NavbarWrapper,
    RecentlyViewed,
    FeedList,
    FooterComponent,
  },
  data() {
    return {
      reachedLast: false,
      recentProducts: []
    }
  },
  methods: {
    handleRecentlyViewedOpen(product) {
      this.$refs.feedList.openProductDetails(product);
    },
    setRecentProducts (products) {
      this.recentProducts = products;
    },
    reachedLastElement() {
      this.reachedLast = true;
    },
    resetLastElement() {
      this.reachedLast = false;
    },
    async loadRecentProducts () {
      const recentlyViewedIds = JSON.parse(localStorage.getItem('recentlyViewed')) || [];

      if (recentlyViewedIds.length === 0) {
        this.recentProducts = []
        return;
      }

      try {
        // Construct the API URL
        const queryParam = recentlyViewedIds.map(id => encodeURIComponent(id)).join(',');
        const apiUrl = `/api/post/posts/bulk?getposts=${queryParam}`;

        // Make the API call
        const response = await axios.get(apiUrl);

        // Populate the `recentProducts` list with the data from the server
        this.recentProducts = response.data;
      } catch (error) {
        console.error("Failed to load recent products:", error);
        this.recentProducts = [];
      }
    }
  },
  mounted() {
    this.loadRecentProducts();
  }

}

</script>
