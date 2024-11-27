<template>
  <NavbarWrapper>
    <Navbar />
    <MyProfileNavbarComponent />
  </NavbarWrapper>
  <MyPostsComponent style="padding-top: 330px"/>
  <FooterComponent />
</template>
<script>
import NavbarWrapper from '@/components/NavbarWrapper.vue';
import Navbar from '@/components/Navbar.vue';
import MyProfileNavbarComponent from '@/components/MyProfile/MyProfileNavbarComponent.vue';
import MyPostsComponent from '@/components/MyProfile/MyPostsComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';
export default {
  components: {
    NavbarWrapper,
    Navbar,
    MyPostsComponent,
    MyProfileNavbarComponent,
    FooterComponent
  }
}
</script>
