<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 to-blue-400 dark:bg-gradient-to-br dark:from-gray-900 dark:to-blue-900 text-white">
    <NewPostHeader />
    <main class="max-w-3xl mx-auto pt-20 pb-24 px-4 sm:px-6 lg:px-8">
      <NewPostImageUpload  :images="images" :imagePreviews="imagePreviews" @close="closeImageSourceDialog" @removeImage="removeImage" @showImageSourceDialog="showImageSourceDialog"/>
      <div class="mb-6">
        <label for="title" class="block text-sm font-medium mb-2 dark:text-blue-300 text-black">Title</label>
        <input
          id="title"
          v-model="title"
          type="text"
          class="w-full px-3 py-2 bg-white dark:bg-black dark:bg-opacity-30 border border-blue-500 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white placeholder-gray-700 dark:placeholder-blue-300"
          placeholder="Enter product title"
        />
        <div v-if="errors.title" class="mt-2 flex items-center space-x-2 bg-red-50 dark:bg-red-900/30 p-2 rounded">
          <AlertCircle class="h-4 w-4 text-red-700 dark:text-red-400" />
          <p class="text-sm text-red-700 dark:text-red-400 font-semibold">{{ errors.title }}</p>
        </div>
      </div>

        <!-- Tags Input -->
      <div class="mb-6">
        <label for="tags" class="block text-sm font-medium mb-2 dark:text-blue-300 text-black">Tags</label>
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
            class="flex-grow px-3 py-2 bg-white dark:bg-black dark:bg-opacity-30 border border-blue-500 rounded-l-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white placeholder-gray-700 dark:placeholder-blue-300"
            placeholder="Enter tags"
          />
          <button @click="addTag" class="btn btn-primary rounded-l-none h-10 w-10 bg-blue-800 dark:bg-blue-500">Add</button>
        </div>
        <div v-if="errors.tags" class="mt-2 flex items-center space-x-2 bg-red-50 dark:bg-red-900/30 p-2 rounded">
          <AlertCircle class="h-4 w-4 text-red-700 dark:text-red-400" />
          <p class="text-sm text-red-700 dark:text-red-400 font-semibold">{{ errors.tags }}</p>
        </div>
      </div>

        <!-- Price Input -->
      <div class="mb-6">
        <label for="price" class="block text-sm font-medium mb-2 dark:text-blue-300 text-black">Price</label>
        <div class="flex items-center">
          <select
            v-model="selectedCurrency"
            class="mr-2 bg-white dark:bg-black dark:bg-opacity-30 border border-blue-500 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white"
          >
            <option v-for="currency in currencies" :key="currency" :value="currency">{{ currency }}</option>
          </select>
          <input
            id="price"
            v-model="price"
            @input="formatPrice"
            @focus="enableCurrencySelection"
            type="text"
            class="flex-grow px-3 py-2 bg-white dark:bg-black dark:bg-opacity-30 border border-blue-500 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white placeholder-gray-700 dark:placeholder-blue-300"
            placeholder="Enter price (min 1,000)"
          />
        </div>
        <div v-if="errors.price" class="mt-2 flex items-center space-x-2 bg-red-50 dark:bg-red-900/30 p-2 rounded">
          <AlertCircle class="h-4 w-4 text-red-700 dark:text-red-400" />
          <p class="text-sm text-red-700 dark:text-red-400 font-semibold">{{ errors.price }}</p>
        </div>
        <div v-if="errors.currency" class="mt-2 flex items-center space-x-2 bg-red-50 dark:bg-red-900/30 p-2 rounded">
          <AlertCircle class="h-4 w-4 text-red-700 dark:text-red-400" />
          <p class="text-sm text-red-700 dark:text-red-400 font-semibold">{{ errors.currency }}</p>
        </div>
        <div v-if="showAdvertisedPrice" class="mt-2 flex items-center space-x-2 bg-blue-50 dark:bg-blue-900/30 p-2 rounded">
          <Info class="h-4 w-4 text-blue-900 dark:text-blue-300" />
          <p class="text-sm text-blue-900 dark:text-blue-300 font-semibold">
            Advertised price with commission: {{ getAdvertisedPrice() }} {{ selectedCurrency }}
          </p>
        </div>
      </div>

        <!-- Quantity Input -->
      <div class="mb-8">
        <label for="quantity" class="block text-sm font-medium mb-2 dark:text-blue-300 text-black">Quantity</label>
        <div class="flex items-center">
          <button
            @click="decrementQuantity"
            class="bg-blue-800 dark:bg-gray-700 text-gray-200 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 h-10 w-10 rounded-l"
          >
            -
          </button>          
          <input
            id="quantity"
            v-model="quantity"
            type="number"
            min="1"
            class="w-20 px-3 py-2 bg-white dark:bg-black dark:bg-opacity-30 border-t border-b border-blue-500 text-center focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white"
          />
          <button
            @click="incrementQuantity"
            class="bg-blue-800 dark:bg-gray-700 text-gray-200 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 h-10 w-10 rounded-r"
          >
            +
          </button>        
        </div>
        <div v-if="showQuantityWarning" class="mt-2 flex items-center space-x-2 bg-blue-50 dark:bg-blue-900/30 p-2 rounded">
          <Info class="h-4 w-4 text-blue-900 dark:text-yellow-400" />
          <p class="text-sm text-blue-900 dark:text-yellow-400 font-semibold">Make sure you have {{ quantity }} items</p>
        </div>
      </div>

        <!-- Action Buttons -->
      <div class="flex justify-between space-x-4">
        <button 
          @click="$router.go(-1)" 
          class="flex-1 px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg shadow-md hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors duration-200 ease-in-out font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 flex items-center justify-center space-x-2"
        >
          <X class="h-5 w-5" />
          <span>Cancel</span>
        </button>
        <button 
          @click="submitPost" 
          :disabled="isLoading" 
          class="flex-1 px-6 py-3 rounded-lg shadow-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center justify-center space-x-2 transition-colors duration-200 ease-in-out"
          :class="[
            isLoading || !isFormValid 
              ? 'bg-blue-400 dark:bg-blue-600 cursor-not-allowed text-white'
              : 'bg-blue-600 dark:bg-blue-500 hover:bg-blue-700 dark:hover:bg-blue-600 text-white'
          ]"
        >
          <template v-if="isLoading">
            <Loader2 class="h-5 w-5 animate-spin" />
            <span>Processing...</span>
          </template>
          <template v-else>
            <Send class="h-5 w-5" />
            <span>Post Item</span>
          </template>
        </button>
      </div>
    </main>
    <NewPostImageSourceDialog :showImageDialog="showImageDialog" @close="closeImageSourceDialog" @selectImageSource="selectImageSource" />
    <NewPostProcessing :progress="progress" :isProcessing="isProcessing" />
    <ReportedNotAllowed v-if="reported" @closeModal="closeNotAllowedModal" :reservation="reportedReservation"/>
    <LoadingComponent v-if="isLoading" :isLoading="isLoading" />
  </div>
</template>

<script>
import NewPostHeader from '@/components/NewPost/NewPostHeader.vue';
import NewPostImageSourceDialog from '@/components/NewPost/NewPostImageSourceDialog.vue';
import NewPostImageUpload from '@/components/NewPost/NewPostImageUpload.vue';
import axios from 'axios'
import NewPostProcessing from '@/components/NewPost/NewPostProcessing.vue';
import ReportedNotAllowed from '@/components/NewPost/ReportedNotAllowed.vue';
import { useToastStore } from '@/stores/toast';
import LoadingComponent from '@/components/NewPost/LoadingComponent.vue';
import { AlertCircle, Info, X, Send, Loader2 } from 'lucide-vue-next'
export default {
  components: {
    NewPostHeader,
    NewPostImageUpload,
    NewPostImageSourceDialog,
    X,
    NewPostProcessing,
    ReportedNotAllowed,
    LoadingComponent,
    AlertCircle,
    Info,
    Send,
    Loader2
  },
  setup() {
    const toastStore = useToastStore();
    return {
      toastStore
    }
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
      reportedReservation: null,
      reported: false,
      isLoading: true,
      errors: {
        images: '',
        title: '',
        tags: '',
        price: '',
        currency: ''
      }
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
      return this.quantity >= 2;
    },
    isValidImageCount() {
      return this.images.length > 0 && this.images.length <= 5;
    },
    formattedPrice() {
      return parseFloat(this.price.replace(/,/g, '')) || 0;
    },
    isFormValid() {
      return this.title.trim() !== '' && this.tags.length >= 3 && this.formattedPrice >= 10 && this.selectedCurrency !== '';
    }
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = {
        images: '',
        title: '',
        tags: '',
        price: '',
        currency: ''
      };

      // Title validation
      if (!this.title.trim()) {
        this.errors.title = 'Title is required';
        isValid = false;
      } else if (this.title.trim().length < 3) {
        this.errors.title = 'Title must be at least 3 characters';
        isValid = false;
      }

      // Tags validation
      if (this.tags.length < 3) {
        this.errors.tags = 'Please add at least 3 tags';
        isValid = false;
      }

      // Price validation
      if (!this.formattedPrice) {
        this.errors.price = 'Price is required';
        isValid = false;
      } else if (this.formattedPrice < 10) {
        this.errors.price = 'Price must be at least $10';
        isValid = false;
      }

      // Currency validation
      if (!this.selectedCurrency) {
        this.errors.currency = 'Please select a currency';
        isValid = false;
      }

      // Image validation
      if (!this.validateImages()) {
        isValid = false;
      }

      if (!isValid) {
        // Show the first error in toast
        const firstError = Object.values(this.errors).find(error => error !== '');
        this.toastStore.showToast(
          5000,
          firstError,
          "bg-red-300 dark:bg-red-300"
        );
      }

      return isValid;
    },
    removeImage(index) {
      this.images.splice(index, 1);
    },
    closeNotAllowedModal() {
      this.$router.push({name: 'home'})
    },
    showImageSourceDialog() {
      this.showImageDialog = true;
    },
    async selectImageSource(source) {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      
      if (source === 'camera') {
        input.capture = 'user'; // Changed from 'environment' to 'user' for front camera
        input.setAttribute('capture', 'user'); // Explicitly set capture attribute
      } else {
        input.removeAttribute('capture'); // Remove capture for gallery
      }

      input.onchange = async (e) => {
        const files = e.target.files;
        if (files.length) {
          for (let i = 0; i < files.length; i++) {
            const file = files[i];
            try {
              const reader = new FileReader();
              
              reader.onload = (event) => {
                // Create an image element to get dimensions
                const img = new Image();
                img.onload = () => {
                  // Only add the image if it loaded successfully
                  this.images.push(file);
                  this.imagePreviews.push(event.target.result);
                };
                img.src = event.target.result;
              };

              reader.onerror = (error) => {
                console.error('Error reading file:', error);
                this.$toast.error('Error reading image file');
              };

              reader.readAsDataURL(file);
            } catch (error) {
              console.error('Error processing image:', error);
              this.$toast.error('Error processing image');
            }
          }
        }
      };

      // Wrap the click in a try-catch to handle any permissions issues
      try {
        input.click();
      } catch (error) {
        console.error('Error opening file picker:', error);
        this.$toast.error('Error accessing camera or gallery');
      }
      
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
    validateImages() {
      if (this.images.length === 0) {
        this.errors.images = 'Please add at least one image';
        return false;
      }
      if (this.images.length > 5) {
        this.errors.images = 'Maximum 5 images allowed';
        return false;
      }
      this.errors.images = '';
      return true;
    },
    async submitPost() {
      if (!this.validateForm()) {
        return;
      }
      
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
        this.$router.push({name: 'myprofile'});
        processingComplete = true;

      }catch(error) {
        console.error('Error generating embeddings:', error);
      } finally {
        const delay = processingComplete ? 2000 : 0; // If processing completes fast, wait for 2 seconds
        await new Promise(resolve => setTimeout(resolve, delay));
        this.isProcessing = false; // Hide the processing modal
      }
    },
    checkReportedOnSeller() {
      this.isLoading = true;
      axios.get('api/account/users/me/')
      .then(
        response => {
          console.log("user", response.data)
          this.isLoading = false;
          const reported_on = response.data.reported;
          this.reported = reported_on;
          if(reported_on){
            this.reportedReservation = response.data.reportedReservation;
          }
        }
      )
      .catch(
        error => {
          this.isLoading = false;
          console.log("erro", error)
          this.toastStore.showToast(
            5000,
            "Something went wrong. Please try again!",
            "bg-red-300 dark:bg-red-300",
          );
        }
      )
    },
  },
  mounted() {
    this.checkReportedOnSeller();
  }
}

</script>
