<template>
  <div class="border-slate-700 px-4 py-3 flex items-center justify-between  p-4">
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
        <div v-show="isSearchExpanded" class="absolute search-bar-wrapper">
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-full text-sm leading-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
            @blur="closeSearch"
          />
          <div class="absolute inset-y-0 left-5 flex items-center pointer-events-none">
            <SearchIcon class="h-5 w-5 text-gray-400" />
          </div>
        </div>
      </div>
      <router-link
        to="/notifications"
        class="p-2 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        aria-label="Notifications"
      >
        <BellIcon class="h-6 w-6" />
      </router-link>
      <span class="text-gray-700 dark:text-gray-200 text-sm">Coins: {{ userCoins }}</span>
      <button
        @click="openBuyCoinsModal"
        class="bg-yellow-500 text-white px-3 py-1 rounded-full text-sm font-medium hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
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

const navbarTransform = ref('0');
const navbarRef = ref<HTMLElement>();
const isSearchExpanded = ref(false);
const searchInput = ref(null)
const searchQuery = ref('')

const userCoins = ref(5)
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

const openBuyCoinsModal = () => {

}

const toggleSearch = () => {
  isSearchExpanded.value = !isSearchExpanded.value
  console.log("is", isSearchExpanded.value)
  if (isSearchExpanded.value) {
    nextTick(() => {
      searchInput.value?.focus
    });
  }
}
const closeSearch = () => {
  if (searchQuery.value === '') {
    isSearchExpanded.value = false
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
