<template>
  <nav class="bg-white dark:bg-gray-800 shadow-lg fixed bottom-0 left-0 right-0 z-10">
      <PwaInstallPrompt />
      <div class="flex justify-around">
          <RouterLink :to="{'name': 'home'}" class="flex flex-col items-center py-2 px-3 text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
            <HomeIcon class="h-6 w-6" />
            <span class="text-xs mt-1">Home</span>
          </RouterLink>
          <RouterLink :to="{'name': 'favourites'}" class="flex flex-col items-center py-2 px-3 text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
            <HeartIcon class="h-6 w-6" />
            <span class="text-xs mt-1">Favourites</span>
          </RouterLink>
          <RouterLink :to="{'name': 'new'}" class="flex flex-col items-center py-2 px-3 text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
            <Plus class="h-6 w-6" />
            <span class="text-xs mt-1">New</span>
          </RouterLink>
          <RouterLink :to="{'name': 'transactions'}" class="flex flex-col items-center py-2 px-3 text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
            <ArrowRightLeft class="h-6 w-6" />
            <span class="text-xs mt-1">Transactions</span>
          </RouterLink>
          <RouterLink :to="{'name': 'myprofile'}" class="flex flex-col items-center py-2 px-3 text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
            <UserIcon class="h-6 w-6" />
            <span class="text-xs mt-1">Profile</span>
          </RouterLink>
        </div>
      </nav>
</template>
<script setup>
import { HomeIcon, ArrowRightLeft, HeartIcon, UserIcon, Plus } from 'lucide-vue-next'
import PwaInstallPrompt from './PwaInstallPrompt.vue';
import { RouterLink } from 'vue-router';

</script>

