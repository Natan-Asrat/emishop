<template>
  <div class="mb-8 bg-black bg-opacity-30 p-6 rounded-lg backdrop-filter backdrop-blur-lg">
    <div v-if="images.length === 0" class="flex justify-center">
      <input type="file" @change="handleFileUpload" multiple accept="image/*" class="hidden" ref="fileInput" />
      <button @click="showImageSourceDialog" class="btn btn-primary">
        <Plus class="h-5 w-5 mr-2" />
        Add Image
      </button>
    </div>
    <div v-else class="flex overflow-x-auto space-x-4 pb-4">
      <div v-for="(image, index) in images" :key="index" class="relative flex-shrink-0">
        <img :src="imagePreviews[index]" alt="Product image" class="w-24 h-24 object-cover rounded-lg shadow-md" />
        <button @click="removeImage(index)" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-2 shadow-md hover:bg-red-600 transition-colors duration-300">
          <X class="h-4 w-4" />
        </button>
      </div>
      <button @click="showImageSourceDialog" class="flex-shrink-0 w-24 h-24 bg-blue-500 bg-opacity-50 rounded-lg flex items-center justify-center shadow-md hover:bg-blue-600 hover:bg-opacity-50 transition-colors duration-300">
        <Plus class="h-8 w-8 text-white" />
      </button>
    </div>
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
const fileInput = ref(null);
const showImageSourceDialog = () => {
  emit('showImageSourceDialog');
};
const removeImage = (index) => {
  emit('removeImage', index);
}
</script>
