<template>
  <NavbarWrapper >

    <Navbar />
    <RecentlyViewed />
  </NavbarWrapper>
  <FeedList />
</template>
<script>
import Navbar from '@/components/Navbar.vue';
import FeedList from '@/components/FeedList.vue';
import RecentlyViewed from '@/components/RecentlyViewed.vue';
import NavbarWrapper from '@/components/NavbarWrapper.vue';
export default {
  name: 'Home',
  components: {
    Navbar,
    NavbarWrapper,
    RecentlyViewed,
    FeedList
  },

}

</script>
