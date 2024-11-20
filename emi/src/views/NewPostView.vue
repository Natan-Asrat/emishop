<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 text-white">
    <NewPostHeader />
    <main class="max-w-3xl mx-auto pt-20 pb-24 px-4 sm:px-6 lg:px-8">
      <NewPostImageUpload  :images="images" :imagePreviews="imagePreviews" @close="closeImageSourceDialog" @removeImage="removeImage" @showImageSourceDialog="showImageSourceDialog"/>
      <div class="mb-6">
        <label for="title" class="block text-sm font-medium mb-2 text-blue-300">Title</label>
        <input
          id="title"
          v-model="title"
          type="text"
          class="w-full px-3 py-2 bg-black bg-opacity-30 border border-blue-500 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-blue-300"
          placeholder="Enter product title"
        />
      </div>

        <!-- Tags Input -->
      <div class="mb-6">
        <label for="tags" class="block text-sm font-medium mb-2 text-blue-300">Tags</label>
        <div class="flex flex-wrap gap-2 mb-2">
          <span
            v-for="(tag, index) in tags"
            :key="index"
            class="bg-blue-500 bg-opacity-50 text-white px-3 py-2 rounded-full text-md flex items-center"
          >
            {{ tag }}
            <button @click="removeTag(index)" class="ml-1 text-white hover:text-blue-200 transition-colors duration-300">
              <X class="h-4 w-4" />
            </button>
          </span>
        </div>
        <div class="flex">
          <input
            id="tags"
            v-model="currentTag"
            @keydown.space.prevent="addTag"
            @keydown.enter.prevent="addTag"
            type="text"
            class="flex-grow px-3 py-2 bg-black bg-opacity-30 border border-blue-500 rounded-l-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-blue-300"
            placeholder="Enter tags"
          />
          <button @click="addTag" class="btn btn-primary rounded-l-none">Add</button>
        </div>
      </div>

        <!-- Price Input -->
      <div class="mb-6">
        <label for="price" class="block text-sm font-medium mb-2 text-blue-300">Price</label>
        <div class="flex items-center">
          <select
            v-model="selectedCurrency"
            class="mr-2 bg-black bg-opacity-30 border border-blue-500 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-white"
          >
            <option v-for="currency in currencies" :key="currency" :value="currency">{{ currency }}</option>
          </select>
          <input
            id="price"
            v-model="price"
            @input="formatPrice"
            @focus="enableCurrencySelection"
            type="text"
            class="flex-grow px-3 py-2 bg-black bg-opacity-30 border border-blue-500 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-blue-300"
            placeholder="Enter price (min 1,000)"
          />
        </div>
        <p v-if="showAdvertisedPrice" class="mt-2 text-sm text-blue-300">
          Advertised price with commission: {{ getAdvertisedPrice() }} {{ selectedCurrency }}
        </p>
      </div>

        <!-- Quantity Input -->
      <div class="mb-8">
        <label for="quantity" class="block text-sm font-medium mb-2 text-blue-300">Quantity</label>
        <div class="flex items-center">
          <button @click="decrementQuantity" class="btn btn-secondary rounded-r-none">-</button>
          <input
            id="quantity"
            v-model="quantity"
            type="number"
            min="1"
            class="w-20 px-3 py-2 bg-black bg-opacity-30 border-t border-b border-blue-500 text-center focus:outline-none focus:ring-2 focus:ring-blue-500 text-white"
          />
          <button @click="incrementQuantity" class="btn btn-secondary rounded-l-none">+</button>
        </div>
        <p v-if="showQuantityWarning" class="mt-2 text-sm text-yellow-400">Make sure you have {{ quantity }} items</p>
      </div>

        <!-- Action Buttons -->
      <div class="flex justify-between">
        <button @click="cancelPost" class="btn btn-secondary">
          Cancel
        </button>
        <button @click="submitPost" class="btn btn-primary">
          Post
        </button>
      </div>
    </main>
    <NewPostImageSourceDialog :showImageDialog="showImageDialog" @close="closeImageSourceDialog" @selectImageSource="selectImageSource" />
    <NewPostProcessing :progress="progress" :isProcessing="isProcessing" />
  </div>
</template>

<script>
import NewPostHeader from '@/components/NewPost/NewPostHeader.vue';
import NewPostImageSourceDialog from '@/components/NewPost/NewPostImageSourceDialog.vue';
import NewPostImageUpload from '@/components/NewPost/NewPostImageUpload.vue';
import { X } from 'lucide-vue-next'
import axios from 'axios'
import NewPostProcessing from '@/components/NewPost/NewPostProcessing.vue';
export default {
  components: {
    NewPostHeader,
    NewPostImageUpload,
    NewPostImageSourceDialog,
    X,
    NewPostProcessing
  },
  data() {
    return {
      showImageDialog: false,
      images: [],
      imagePreviews: [],
      title: '',
      tags: [],
      currentTag: '',
      selectedCurrency: '',
      price: '',
      currencies: ['USD', 'EUR', 'GBP', 'JPY'],
      quantity: 1,
      isProcessing: false,
      commissionRate: 0.01,
      progress: 'Downloading AI model',

    }
  },
  computed: {
    showAdvertisedPrice() {
      return parseFloat(this.price.replace(/,/g, '')) >= 1000;
    },
    getAdvertisedPrice() {
      const actualPrice = parseFloat(this.price.replace(/,/g, ''));
      return ((actualPrice / (1 - this.commissionRate))).toFixed(2);
    },
    showQuantityWarning() {
      return this.quantity >= 2
    },
  },
  methods: {
    removeImage(index) {
      this.images.splice(index, 1);
    },
    showImageSourceDialog() {
      this.showImageDialog = true;
    },
    selectImageSource(source) {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      if (source === 'camera') {
        input.capture = 'environment';
      }
      input.onchange = (e) => {
        const files = e.target.files;
        if (files.length) {
          for (let i = 0; i < files.length; i++) {
            const file = files[i];
              const reader = new FileReader();

              reader.onload = (event) => {
                this.images.push(file);
                this.imagePreviews.push(event.target.result);
              };

              reader.readAsDataURL(file);
          }
        }
      };
      input.click();
      this.closeImageSourceDialog();
    },
    closeImageSourceDialog() {
      this.showImageDialog = false;
    },
    removeTag(index) {
      this.tags.splice(index, 1);
    },
    addTag() {
      if (this.currentTag.trim()) {
        this.tags.push(this.currentTag.trim());
        this.currentTag = '';
      }
    },
    formatPrice() {
      let numericPrice = this.price.replace(/[^0-9]/g, '');

      this.price = numericPrice.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    enableCurrencySelection () {
      if (!this.selectedCurrency) {
        this.selectedCurrency = this.currencies[0];
      }
    },
    decrementQuantity () {
      if (this.quantity > 1) {
        this.quantity--;
      }
    },
    incrementQuantity () {
      this.quantity++;
    },
    async submitPost() {
      this.isProcessing = true;
      let processingComplete = false;
      try{
        await import('@tensorflow/tfjs');
        const use = await import('@tensorflow-models/universal-sentence-encoder');
        const model = await use.load()
        this.progress = 'Generating embeddings'
        const embeddings = await model.embed(this.tags);
        this.progress = 'Uploading post'
        const tagEmbeddings = embeddings.arraySync(); // Convert to a JavaScript array

        const averageEmbedding = tagEmbeddings.reduce((acc, curr) =>
          acc.map((val, i) => val + curr[i]), new Array(512).fill(0))
          .map(val => val / tagEmbeddings.length);
        const formData = new FormData();
        formData.append('title', this.title);
        formData.append('price', parseFloat(this.price.replace(/,/g, '')) || null);
        formData.append('currency', this.selectedCurrency);
        formData.append('quantity', this.quantity || null);
        formData.append('tags', JSON.stringify(this.tags)); // Assuming tags are sent as a JSON string
        averageEmbedding.forEach((value, index) => {
          formData.append(`embedding[${index}]`, value);  // Send each float as a separate field
        });
        this.images.forEach(image => {
          formData.append('images', image); // Ensure these are File objects
        });

        await axios.post(`api/post/posts/create-new/`, formData);
        this.$router.push('/myprofile');
        processingComplete = true;

      }catch(error) {
        console.error('Error generating embeddings:', error);
      } finally {
        const delay = processingComplete ? 2000 : 0; // If processing completes fast, wait for 2 seconds
        await new Promise(resolve => setTimeout(resolve, delay));
        this.isProcessing = false; // Hide the processing modal
      }
    }
  }
}

</script>
