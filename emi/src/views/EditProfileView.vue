<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md space-y-8">
      <button @click="$router.push({name: 'myprofile'})" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
          <XIcon class="h-6 w-6 text-white" />
        </button>
      <div class="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">
        <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-gray-100 mb-6">
          Edit Profile
        </h2>
        <h2 class="text-sm text-center text-gray-700 dark:text-gray-300 mb-6">
          You can change nickname but not username, you'll still use the old username on signin!
        </h2>
        <p class="text-center text-gray-600 dark:text-gray-400 mb-8">
          Update your profile details below
        </p>

        <!-- Error Messages -->
        <div v-if="errors.length" class="mb-4">
          <ul class="text-sm text-red-600 dark:text-red-400 list-disc pl-5 space-y-1">
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
          </ul>
        </div>

        <form @submit.prevent="submitForm" class="space-y-6">
          <div class="space-y-4">
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
                />
                <button 
                  type="button"
                  @click="showImageSourceDialog()"
                  class="relative group cursor-pointer"
                >
                  <img loading="lazy" 
                    v-if="avatarPreview || userStore.user.avatar" 
                    :src="avatarPreview || userStore.user.avatar" 
                    class="h-20 w-20 rounded-full object-cover border-2 border-gray-200 group-hover:opacity-75 transition-opacity"
                    alt="Avatar preview"
                  />
                  <div 
                    v-else 
                    class="h-20 w-20 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center group-hover:bg-gray-300 dark:group-hover:bg-gray-600 transition-colors"
                  >
                    <span class="text-gray-500 dark:text-gray-400">Upload</span>
                  </div>
                </button>
              </div>
            </div>

            <div class="space-y-2">
              <label for="name" class="text-sm font-medium text-gray-700 dark:text-gray-300">Nickname</label>
              <input
                v-model="form.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="Your nickname"
                id="name"
              />
            </div>

            <div v-if="changePassword" class="space-y-4">
              <div class="space-y-2">
                <label for="password1" class="text-sm font-medium text-gray-700 dark:text-gray-300">New Password</label>
                <input
                  v-model="form.password1"
                  type="password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  placeholder="New password"
                  id="password1"
                />
              </div>
              <div class="space-y-2">
                <label for="password2" class="text-sm font-medium text-gray-700 dark:text-gray-300">Confirm Password</label>
                <input
                  v-model="form.password2"
                  type="password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  placeholder="Confirm new password"
                  id="password2"
                />
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <input
                type="checkbox"
                v-model="changePassword"
                id="change_password"
                class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:bg-gray-700 dark:border-gray-600"
              />
              <label for="change_password" class="text-sm text-gray-700 dark:text-gray-300">
                Change Password
              </label>
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>

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
import { reactive, ref, defineExpose } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import { XIcon } from "lucide-vue-next";
import ImageSourceDialog from '@/components/ImageSourceDialog.vue';
import WebRTCCamera from '@/components/WebRTCCamera.vue';

const router = useRouter();
const userStore = useUserStore();
const toastStore = useToastStore();

const form = reactive({
  name: userStore.user.name || "",
  password1: "",
  password2: "",
  avatar: null,
});

const changePassword = ref(false);
const errors = reactive([]);
const avatarPreview = ref(null);
const fileInput = ref(null);
const showImageDialog = ref(false);
const showWebRTCCamera = ref(false);

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
    // Trigger file input for gallery selection
    if (fileInput.value) {
      fileInput.value.click();
    }
  }
}

const handleWebRTCImageCapture = (imageData) => {
  // Convert base64 to File object
  const blob = dataURItoBlob(imageData);
  const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
  
  // Update avatar preview and file
  form.avatar = file;
  avatarPreview.value = imageData;
  
  // Close camera modal
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

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    form.avatar = file;
    avatarPreview.value = URL.createObjectURL(file);
  }
};

const submitForm = async () => {
  errors.splice(0); // Clear errors
  if (changePassword.value && form.password1 !== form.password2) {
    errors.push("Passwords do not match");
    return;
  }

  const formData = new FormData();
  formData.append("name", form.name);
  if (changePassword.value) {
    formData.append("password1", form.password1);
    formData.append("password2", form.password2);
  }
  if (form.avatar) {
    formData.append("avatar", form.avatar);
  }

  try {
    const response = await axios.patch("/api/account/users/update_profile/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    if (response.status === 200) {
      toastStore.showToast(5000, "Profile updated successfully!", "bg-green-500");
      userStore.setUserInfo(response.data);
      router.push({name: 'myprofile'})

    }
  } catch (error) {
    errors.push(error.response?.data?.message || "An error occurred.");
  }
};

// Expose fileInput ref to template
defineExpose({
  fileInput
});
</script>
