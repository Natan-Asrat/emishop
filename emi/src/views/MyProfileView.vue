<template>
  <NavbarWrapper>
    <Navbar />
    <MyProfileNavbarComponent />
  </NavbarWrapper>
  <MyPostsComponent style="padding-top: 330px"/>
</template>
<script>
import NavbarWrapper from '@/components/NavbarWrapper.vue';
import Navbar from '@/components/Navbar.vue';
import MyProfileNavbarComponent from '@/components/MyProfile/MyProfileNavbarComponent.vue';
import MyPostsComponent from '@/components/MyProfile/MyPostsComponent.vue';
export default {
  components: {
    NavbarWrapper,
    Navbar,
    MyPostsComponent,
    MyProfileNavbarComponent
  }
}
</script>
