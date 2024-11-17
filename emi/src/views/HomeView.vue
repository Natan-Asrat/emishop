<template>
  <NavbarWrapper @reachedLastElement="reachedLastElement">

    <Navbar />
    <RecentlyViewed />
  </NavbarWrapper>
  <FeedList :reachedLast="reachedLast" @resetLastElement="resetLastElement" />
  <FooterComponent />
</template>
<script>
import Navbar from '@/components/Navbar.vue';
import FeedList from '@/components/FeedList.vue';
import RecentlyViewed from '@/components/RecentlyViewed.vue';
import NavbarWrapper from '@/components/NavbarWrapper.vue';
import FooterComponent from '@/components/FooterComponent.vue';
export default {
  name: 'Home',
  components: {
    Navbar,
    NavbarWrapper,
    RecentlyViewed,
    FeedList,
    FooterComponent
  },
  data() {
    return {
      reachedLast: false
    }
  },
  methods: {
    reachedLastElement() {
      this.reachedLast = true;
    },
    resetLastElement() {
      this.reachedLast = false;
    }
  }

}

</script>
