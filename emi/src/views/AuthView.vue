<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md space-y-8">
      <p class="text-center dark:text-white mt-4 w-[80%] mx-auto">If you're having problems, please set Chrome as your default browser.</p>
      <div class="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">
        <div>
          <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-gray-100 mb-6">
            {{ isSignUp ? 'Create your account' : 'Welcome back' }}
          </h2>
          <p class="text-center text-gray-600 dark:text-gray-400 mb-8">
            {{ isSignUp ? 'Enter your details to get started' : 'Enter your credentials to access your account' }}
          </p>

          <!-- Error Messages -->
          <div v-if="errors.length" class="mb-4">
            <ul class="text-sm text-red-600 dark:text-red-400 list-disc pl-5 space-y-1">
              <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
            </ul>
          </div>

          <form @submit.prevent="handleAuth" class="space-y-6">
            <div class="space-y-4">

              <template v-if="isSignUp">

                <div class="flex flex-col items-center space-y-2">
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Avatar</label>
                  <div class="flex items-center justify-center">
                    <input
                      type="file"
                      @change="handleFileChange"
                      accept="image/*"
                      class="hidden"
                      id="avatar"
                      ref="fileInput"
                      :disabled="isLoading"
                    />
                    <button 
                      type="button"
                      @click="showImageSourceDialog()"
                      :disabled="isLoading"
                      class="relative group cursor-pointer disabled:cursor-not-allowed"
                    >
                      <img loading="lazy" 
                        v-if="avatarPreview" 
                        :src="avatarPreview" 
                        class="h-20 w-20 rounded-full object-cover border-2 border-gray-200 group-hover:opacity-75 transition-opacity"
                        alt="Avatar preview"
                      />
                      <div 
                        v-else 
                        class="h-20 w-20 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center group-hover:bg-gray-300 dark:group-hover:bg-gray-600 transition-colors"
                      >
                        <svg 
                          class="h-10 w-10 text-gray-400" 
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                        >
                          <path 
                            stroke-linecap="round" 
                            stroke-linejoin="round" 
                            stroke-width="2" 
                            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                          />
                        </svg>
                      </div>
                      <!-- Overlay with camera icon -->
                      <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <div class="rounded-full bg-black bg-opacity-50 p-2">
                          <svg 
                            class="h-6 w-6 text-white" 
                            fill="none" 
                            stroke="currentColor" 
                            viewBox="0 0 24 24"
                          >
                            <path 
                              stroke-linecap="round" 
                              stroke-linejoin="round" 
                              stroke-width="2" 
                              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                            />
                            <path 
                              stroke-linecap="round" 
                              stroke-linejoin="round" 
                              stroke-width="2" 
                              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                            />
                          </svg>
                        </div>
                      </div>
                    </button>
                  </div>
                  <p class="text-center text-xs text-gray-500 dark:text-gray-400 mt-2">
                    Click to choose an avatar
                  </p>
                </div>
              </template>
              <div class="space-y-2">
                <label for="username" class="text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
                <input
                  id="username"
                  v-model="user.username"
                  type="text"
                  required
@input="user.username = user.username.toLowerCase()"
autocapitalize="none"
                  :disabled="isLoading"
                  :class="{'border-red-500': errors.username}"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
                  placeholder="Enter your username"
                />
              </div>
              <div class="space-y-2">
                <label for="password" class="text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
                <input
                  v-model="user.password1"
                  type="password"
                  placeholder="Your password"
                  :disabled="isLoading"
                  :class="{'border-red-500': errors.password1}"
                  class="w-full py-4 px-6 border border-gray-200 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  id="password"
                />
              </div>
              <template v-if="isSignUp">
                <div class="space-y-2">
                  <label for="password2" class="text-sm font-medium text-gray-700 dark:text-gray-300">Repeat password</label>
                  <input
                    v-model="user.password2"
                    type="password"
                    placeholder="Confirm password"
                    :disabled="isLoading"
                    :class="{'border-red-500': errors.password2}"
                    class="w-full py-4 px-6 border border-gray-200 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    id="password2"
                  />
                </div>
                <div class="space-y-2">
                  <label for="nickname" class="text-sm font-medium text-gray-700 dark:text-gray-300">Nickname</label>
                  <input
                    id="nickname"
                    v-model="user.nickname"
                    type="text"
                    required
                    :disabled="isLoading"
                    :class="{'border-red-500': errors.nickname}"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
                    placeholder="Choose a nickname"
                  />
                </div>
              </template>
            </div>
            <div>
              <button
                type="submit"
                :disabled="isLoading"
                class="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg 
                  v-if="isLoading" 
                  class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" 
                  xmlns="http://www.w3.org/2000/svg" 
                  fill="none" 
                  viewBox="0 0 24 24"
                >
                  <circle 
                    class="opacity-25" 
                    cx="12" 
                    cy="12" 
                    r="10" 
                    stroke="currentColor" 
                    stroke-width="4"
                  ></circle>
                  <path 
                    class="opacity-75" 
                    fill="currentColor" 
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                {{ isSignUp ? 'Create Account' : 'Sign In' }}
              </button>
            </div>
          </form>
        </div>
      </div>
      <div class="text-center mt-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
          <button
            @click="toggleAuthMode"
            :disabled="isLoading"
            class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSignUp ? 'Sign In' : 'Sign Up' }}
          </button>
        </p>
      </div>
    </div>

    <!-- Error Modal -->
    <TransitionRoot appear :show="isErrorModalOpen" as="template">
      <Dialog as="div" @close="closeErrorModal" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle
                  as="h3"
                  class="text-lg font-medium leading-6 text-gray-900 dark:text-white"
                >
                  {{ errorTitle }}
                </DialogTitle>
                <div class="mt-2">
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ errorMessage }}
                  </p>
                </div>

                <div class="mt-4">
                  
                  <Transition
                    as="div"
                    v-if="isDropdownOpen"
                    :show="isDropdownOpen"
                    enter="transition ease-out duration-200"
                    enter-from="opacity-0 translate-y-1"
                    enter-to="opacity-100 translate-y-0"
                    leave="transition ease-in duration-150"
                    leave-from="opacity-100 translate-y-0"
                    leave-to="opacity-0 translate-y-1"
                  >
                    <div class="mt-2 p-4 rounded-md bg-gray-100 text-sm text-gray-700 dark:bg-gray-700 dark:text-gray-300">
                      {{ errorDetails }}
                    </div>
                  </Transition>
                </div>

                <div class="mt-4 flex justify-between">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="closeErrorModal"
                  >
                    Got it
                  </button>
                  <button
                    type="button"
                    v-if="errorDetails"
                    @click="isDropdownOpen = !isDropdownOpen"
                    class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
                  >
                  {{ isDropdownOpen ? 'Hide Details' : 'View Details'}}
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>


    <ImageSourceDialog 
      :isOpen="showImageDialog" 
      @close="closeImageSourceDialog" 
      @select-source="selectImageSource" 
    />
    <WebRTCCamera 
      v-if="showWebRTCCamera" 
      @close="closeCameraModal"
      @image-confirmed="handleWebRTCImageCapture"
    />
  </div>
</template>

<script setup>
import { ref, reactive, defineExpose } from 'vue'
import axios from 'axios';
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import ImageSourceDialog from '@/components/ImageSourceDialog.vue';
import WebRTCCamera from '@/components/WebRTCCamera.vue';

const fileInput = ref(null);
const userStore = useUserStore();
const toastStore = useToastStore();
const isSignUp = ref(false);
const isLoading = ref(false);
const isErrorModalOpen = ref(false);
const isDropdownOpen = ref(false);
const errorTitle = ref('');
const errorDetails = ref('');
const errorMessage = ref('');
const avatarPreview = ref('');
const showImageDialog = ref(false);
const showWebRTCCamera = ref(false);
const avatarFile = ref(null);

const user = reactive({
  username: '',
  nickname: '',
  password1: "",
  password2: "",
  avatar: null,
});

const errors = reactive({
  username: null,
  nickname: null,
  password1: null,
  password2: null,
  avatar: null,
  general: null,
});

const emit = defineEmits(['auth-success']);

const closeErrorModal = () => {
  isErrorModalOpen.value = false;
};

const showError = (title, message, description='') => {
  errorTitle.value = title;
  errorMessage.value = message;
  isErrorModalOpen.value = true;
  if(description) {
    errorDetails.value = description;
  }
};

const toggleAuthMode = () => {
  if (isLoading.value) return;
  isSignUp.value = !isSignUp.value;
  Object.keys(user).forEach(key => user[key] = '');
  Object.keys(errors).forEach(key => errors[key] = null);
  avatarPreview.value = '';
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (!file.type.match('image.*')) {
      showError('Invalid File', 'Please select an image file');
      event.target.value = '';
      return;
    }
    
    avatarFile.value = file;
    avatarPreview.value = URL.createObjectURL(file);
  }
};

const validateForm = () => {
  const errors = {
    username: null,
    nickname: null,
    password1: null,
    password2: null,
    avatar: null,
  };

  if (isSignUp.value) {
    if (!user.nickname) errors.nickname = "Your name is missing";
    if (!user.username) errors.username = "Your username is missing";
    if (!user.password1) errors.password1 = "Your password is missing";
    if (!user.password2) errors.password2 = "Confirm your password";
    if (user.password1.length < 8) errors.password1 = "Password must be at least 8 characters long";
    if (user.password1 !== user.password2) errors.password2 = "Passwords do not match";
    if (!avatarFile.value) errors.avatar = "Please select an avatar";

    if (Object.values(errors).some((error) => error)) {
      showError('Validation Error', Object.values(errors).find(error => error));
      return false;
    }
  } else {
    if (!user.username) errors.username = "Your username is missing";
    if (!user.password1) errors.password1 = "Your password is missing";

    if (Object.values(errors).some((error) => error)) {
      showError('Validation Error', Object.values(errors).find(error => error));
      return false;
    }
  }

  return true;
};

const handleAuth = async () => {
  if (isLoading.value) return;

  if (!validateForm()) return;
  isLoading.value = true;
  
  const action = isSignUp.value ? 'signup' : 'signin';

  try {
    if (action === 'signup') {
      const formData = new FormData();
      formData.append("username", user.username);
      formData.append("name", user.nickname);
      formData.append("password1", user.password1);
      formData.append("password2", user.password2);
      if (avatarFile.value) formData.append("avatar", avatarFile.value);

      const response = await axios.post("/api/account/users/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.status === 201) {
        toastStore.showToast(5000, "The user is registered. Please log in!", "bg-green-500 dark:bg-green-500");
        userStore.setUserInfo(response.data);
        isSignUp.value = false;
      } else {
        showError('Registration Error', "Something went wrong. Please try again!");
      }
    } else if (action === 'signin') {
      const response = await axios.post("/api/account/login/", {
        username: user.username,
        password: user.password1,
      });

      userStore.setToken(response.data);
      axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;

      toastStore.showToast(5000, "You are logged in successfully!", "bg-green-500 dark:bg-green-500");
      if (response.status === 200) {
        userStore.setUserInfo(response.data);
        emit('auth-success');
        const response2 = await axios.get("/api/account/users/me/");
        if (response.status === 200) {
          userStore.setUserInfo(response2.data);
        }
      } else {
        showError('Login Error', "Something went wrong. Please try again!");
      }
    }
  } catch (error) {
    if (action === 'signup') {
      const errorMessage = error.response?.data?.username?.[0] || 
                         error.response?.data?.message || 
                         "An error occurred during registration.";
      showError('Registration Error', errorMessage, error);
    } else {
      showError('Login Error', error.response?.data?.message || "Invalid login credentials");
    }
  } finally {
    isLoading.value = false;
  }
};

const showImageSourceDialog = () => {
  showImageDialog.value = true;
}

const closeImageSourceDialog = () => {
  showImageDialog.value = false;
}

const selectImageSource = (source) => {
  closeImageSourceDialog();
  if (source === 'camera') {
    showWebRTCCamera.value = true;
  } else if (source === 'gallery') {
    if (fileInput.value) {
      fileInput.value.click();
    }
  }
}

const handleWebRTCImageCapture = (imageData) => {
  const blob = dataURItoBlob(imageData);
  const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
  
  avatarFile.value = file;
  avatarPreview.value = imageData;
  
  closeCameraModal();
}

const closeCameraModal = () => {
  showWebRTCCamera.value = false;
}

const dataURItoBlob = (dataURI) => {
  const byteString = atob(dataURI.split(',')[1]);
  const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  
  return new Blob([ab], { type: mimeString });
}

defineExpose({
  fileInput
});
</script>
