<template>
  <div class="border-slate-700 px-4 py-3 bg-gray-100 dark:bg-gray-800 flex items-center justify-between  p-4">
    <div class="flex-shrink-0">
      <img class="h-12 w-12 rounded" :src="logo" alt="Logo" />
    </div>
    <div class="flex items-center space-x-4">
      <div class="relative search-container">
        <button
          @click="toggleSearch"
          class="p-2 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          aria-label="Open search"
        >
          <SearchIcon class="h-6 w-6" />
        </button>
        <div v-show="feedPostStore.isSearchExpanded" class="absolute search-bar-wrapper ">
          <form @submit.prevent="search">
            <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-full text-sm leading-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
            @blur="closeSearch"
          />
          </form>

          <div class="absolute inset-y-0 left-5 flex items-center pointer-events-none">
            <SearchIcon class="h-5 w-5 text-gray-400" />
          </div>
        </div>
      </div>
      <router-link
        :to="{'name': 'notifications'}"
        class="p-2 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        aria-label="Notifications"
      >
        <BellIcon class="h-6 w-6" />
      </router-link>
      <span class="text-gray-700 dark:text-gray-200 text-sm">Coins: {{ userStore.user.coins }}</span>
      <button
        @click="redirectToBuyCoins"
        class="bg-yellow-500 text-gray-900 px-3 py-1 rounded-full text-sm font-medium hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
      >
        Buy Coins
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import logo from '@/assets/logo.png';
import { SearchIcon, BellIcon } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user';
import { useFeedPostStore } from '@/stores/feedPost';
import {useRouter} from 'vue-router'
import axios from 'axios';
const feedPostStore = useFeedPostStore();
const navbarTransform = ref('0');
const navbarRef = ref<HTMLElement>();
const searchInput = ref(null)
const searchQuery = ref('')
const userStore = useUserStore()
const router = useRouter()
let lastScroll = 0;
let isScrollingDown = false;

// Start calculating scroll direction and apply translateY
const handleScroll = () => {
    const navbarH = navbarRef.value?.clientHeight as number;
    const currentScroll = window.scrollY;

    if (currentScroll > lastScroll && !isScrollingDown) {
        // scrolling down
        isScrollingDown = true;
        navbarTransform.value = `-${navbarH}px`;  // Hide the navbar
    } else if (currentScroll < lastScroll && isScrollingDown) {
        // scrolling up
        isScrollingDown = false;
        navbarTransform.value = '0';  // Show the navbar
    }

    lastScroll = currentScroll <= 0 ? 0 : currentScroll; // Prevent negative scroll values
};

const redirectToBuyCoins = () => {
  router.push({name: 'buy-coins'})
}
const search = () => {
  if (searchQuery.value.trim()) {
    axios.get(`/api/post/posts/?search=${searchQuery.value}`)
    .then(response => {
        // Handle the response (e.g., update the UI with search results)
        const results = response.data.map(post => ({
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
        feedPostStore.setSearchresults(results)
      })
      .catch(error => {
        // Handle any errors
        console.error("There was an error with the search:", error);
      });
  }else{
    feedPostStore.setSearchresults([])
  }
}

const toggleSearch = () => {
  feedPostStore.toggleSearch()
  if (feedPostStore.isSearchExpanded) {
    nextTick(() => {
      searchInput.value?.focus
    });
  }
}
const closeSearch = () => {
  if (searchQuery.value === '') {
    feedPostStore.setSearchExpanded(false)
  }
}

onMounted(() => {
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.navbar {
  transition: transform 0.3s;
}

.navbar.hidden {
  transform: translateY(-100%);
}
</style>
<style scoped>
.loader {
border: 5px solid #f3f3f3; /* Light grey */
border-top: 5px solid #3498db; /* Blue */
border-radius: 50%;
width: 50px;
height: 50px;
animation: spin 1s linear infinite;
}

@keyframes spin {
0% { transform: rotate(0deg); }
100% { transform: rotate(360deg); }
}
main {
  transition: padding 0.3s ease;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease-out;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
.search-container {
position: static;
}

.search-bar-wrapper {
position: absolute;
top: 100%;
left: 50%;
transform: translateX(-50%);
width: calc(100% - 2rem);
max-width: 600px;
padding: 0.5rem 1rem;
background-color: inherit;
z-index: 20;
}

@media (max-width: 640px) {
.search-bar-wrapper {
  width: calc(100% - 1rem);
  padding: 0.5rem;
}
}
</style>
