<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-2">
      <label class="block text-sm font-medium dark:text-blue-300 text-black">Images</label>
      <span class="text-sm dark:text-blue-300 text-black">{{ images.length }}/5 images</span>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-4">
      <div v-for="(preview, index) in imagePreviews" :key="index" class="relative aspect-square">
        <img loading="lazy" :src="preview" alt="Preview" class="w-full h-full object-cover rounded-lg" />
        <button
          @click="$emit('removeImage', index)"
          class="absolute top-2 right-2 p-1 bg-red-500 rounded-full text-white hover:bg-red-600 transition-colors duration-300"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
      <button
        v-if="images.length < 5"
        @click="$emit('showImageSourceDialog')"
        class="aspect-square flex items-center justify-center border-2 border-dashed dark:border-blue-500 border-blue-800 rounded-lg hover:bg-blue-500 hover:bg-opacity-10 transition-colors duration-300"
      >
        <Plus class="h-8 w-8 dark:text-blue-400 text-blue-800" />
      </button>
    </div>
    <p class="text-sm dark:text-blue-300 text-black">Add up to 5 images of your product</p>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps } from 'vue';
import { Plus, X } from 'lucide-vue-next'
const emit = defineEmits(['removeImage', 'showImageSourceDialog']);
defineProps({
  imagePreviews: {
    type: Array,
    required: true
  },
  images: {
    type: Array,
    required: true
  },
});
</script>
