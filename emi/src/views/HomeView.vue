<template>
  <NavbarWrapper >

    <Navbar />
    <RecentlyViewed />
  </NavbarWrapper>
  <!-- <FeedList /> -->
   <div style="margin-top: 200px; height: 200vh">jeyy</div>
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
