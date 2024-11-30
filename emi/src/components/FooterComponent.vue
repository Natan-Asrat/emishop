<template>
  <nav class="bg-white dark:bg-gray-800 shadow-lg fixed bottom-0 left-0 right-0 z-10">
    <PwaInstallPrompt />  
    <div class="flex justify-around">
        <router-link 
          to="/" 
          class="flex flex-col items-center py-2 px-3 transition-colors duration-200" 
          :class="[
            $route.name === 'home'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <HomeIcon class="h-6 w-6" />
          <span class="text-xs mt-1">Home</span>
        </router-link>
        <router-link 
          to="/favourites" 
          class="flex flex-col items-center py-2 px-3 transition-colors duration-200"
          :class="[
            $route.name === 'favourites'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <HeartIcon class="h-6 w-6" />
          <span class="text-xs mt-1">Favourites</span>
        </router-link>
        <router-link 
          to="/new" 
          class="flex flex-col items-center py-2 px-3 transition-colors duration-200"
          :class="[
            $route.name === 'new'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <Plus class="h-6 w-6" />
          <span class="text-xs mt-1">New</span>
        </router-link>
        <router-link 
          to="/transactions" 
          class="flex flex-col items-center py-2 px-3 transition-colors duration-200"
          :class="[
            $route.name === 'transactions'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <ArrowRightLeft class="h-6 w-6" />
          <span class="text-xs mt-1">Transactions</span>
        </router-link>
        <router-link 
          to="/myprofile" 
          class="flex flex-col items-center py-2 px-3 transition-colors duration-200"
          :class="[
            $route.name === 'myprofile'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <UserIcon class="h-6 w-6" />
          <span class="text-xs mt-1">Profile</span>
        </router-link>
      </div>
    </nav>
</template>

<script setup>
import { HomeIcon, ArrowRightLeft, HeartIcon, UserIcon, Plus } from 'lucide-vue-next'
import PwaInstallPrompt from './PwaInstallPrompt.vue';
import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
const $route = useRoute()
</script>
