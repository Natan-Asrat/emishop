<template>
  <nav class="bg-gray-100 dark:bg-gray-900 fixed top-0 left-0 right-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button class="dark:text-gray-100 text-gray-900 hover:text-gray-700 transition-colors duration-300">
              <ArrowLeft class="h-6 w-6" @click="$router.go(-1)" />
            </button>
            <h1 class="ml-4 text-xl font-semibold text-gray-900 dark:text-gray-100">New Post</h1>
          </div>
        </div>
      </div>
    </nav>
</template>
<script setup>
import { ArrowLeft }  from 'lucide-vue-next'
</script>
