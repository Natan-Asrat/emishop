<template>
  <nav class="bg-black bg-opacity-50 backdrop-filter backdrop-blur-lg fixed top-0 left-0 right-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button class="text-blue-400 hover:text-blue-300 transition-colors duration-300">
              <ArrowLeft class="h-6 w-6" />
            </button>
            <h1 class="ml-4 text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">New Post</h1>
          </div>
        </div>
      </div>
    </nav>
</template>
<script setup>
import { ArrowLeft }  from 'lucide-vue-next'
</script>
