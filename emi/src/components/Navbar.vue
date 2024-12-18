<template>
  <div class="border-slate-700 px-4 py-3 bg-gray-100 dark:bg-gray-800 flex items-center justify-between  p-4">
    <div class="flex-shrink-0">
      <img loading="lazy" class="h-12 w-12 rounded" :src="logo" alt="Logo" />
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
            @keyup.enter="search"
          />
          </form>

          <div class="absolute inset-y-0 left-5 flex items-center pointer-events-none">
            <SearchIcon class="h-5 w-5 text-gray-400" />
          </div>
          <div v-if="isSearching" class="absolute inset-0 flex items-center justify-center">
            <Loader2 class="w-12 h-12 text-white animate-spin" />
          </div>
          <div v-if="noResults && !isSearching" class="absolute inset-0 flex items-center justify-center">
            <div class="text-gray-700 dark:text-gray-200 text-sm font-semibold bg-gray-800 bg-opacity-75 px-6 py-4 rounded-lg">
              No results found for "{{ searchQuery }}"
            </div>
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
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import logo from '@/assets/logo.png';
import { SearchIcon, BellIcon, Loader2 } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user';
import { useFeedPostStore } from '@/stores/feedPost';
import {useRouter} from 'vue-router'
import axios from 'axios';
import { getPostData } from '@/utils';
const feedPostStore = useFeedPostStore();
const navbarTransform = ref('0');
const navbarRef = ref<HTMLElement>();
const searchInput = ref(null)
const searchQuery = ref('')
const userStore = useUserStore()
const router = useRouter()
let lastScroll = 0;
let isScrollingDown = false;
const isSearching = ref(false);
const noResults = ref(false);

const handleScroll = () => {
    const navbarH = navbarRef.value?.clientHeight as number;
    const currentScroll = window.scrollY;

    if (currentScroll > lastScroll && !isScrollingDown) {
        isScrollingDown = true;
        navbarTransform.value = `-${navbarH}px`;
    } else if (currentScroll < lastScroll && isScrollingDown) {
        isScrollingDown = false;
        navbarTransform.value = '0';
    }

    lastScroll = currentScroll <= 0 ? 0 : currentScroll;
};

const redirectToBuyCoins = () => {
  router.push({name: 'buy-coins'})
}
const search = () => {
  if (!searchQuery.value || isSearching.value || !feedPostStore.hasMoreSearchResults) return;
  isSearching.value = true;
  noResults.value = false;
  feedPostStore.searchPage++;
  axios.get(`/api/post/posts/?search=${searchQuery.value}&page=${feedPostStore.searchPage}`)
    .then(response => {
        const results = response.data.results.map(post => (getPostData(post)))
        feedPostStore.setSearchresults(results)
        feedPostStore.hasMoreSearchResults = response.data.next !== null

        noResults.value = results.length === 0;
      })
      .catch(error => {
        console.error("There was an error with the search:", error);
      })
      .finally(() => {
        isSearching.value = false;
      });
}
const toggleSearch = () => {
  feedPostStore.toggleSearch()
  if (feedPostStore.isSearchExpanded) {
    nextTick(() => {
      searchInput.value?.focus()
    });
  }
}
const closeSearch = () => {
  if (searchQuery.value === '') {
    feedPostStore.setSearchExpanded(false)
  }
  noResults.value = false;
}

onMounted(() => {
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});
defineExpose({
  searchMore: () => {
    search()
  }
})
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
