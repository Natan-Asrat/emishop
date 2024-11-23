<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md space-y-8">
      <div class="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">
        <div >
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

                <div class="space-y-2">
                <label for="avatar" class="text-sm font-medium text-gray-700 dark:text-gray-300">Avatar</label>
                <input
                  type="file"
                  @change="handleFileChange"
                  class="w-full py-4 px-6 border border-gray-200 rounded-lg"
                  id="avatar"
                />
              </div>
              </template>
              <div class="space-y-2">
                <label for="username" class="text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
                <input
                  id="username"
                  v-model="user.username"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  placeholder="Enter your username"
                />
              </div>
              <div class="space-y-2">
                <label for="password" class="text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
                <input
                  v-model="user.password1"
                  type="password"
                  placeholder="Your password"
                  class="w-full py-4 px-6 border border-gray-200 rounded-lg"
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
                    class="w-full py-4 px-6 border border-gray-200 rounded-lg"
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
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    placeholder="Choose a nickname"
                  />
                </div>
              </template>
            </div>
            <div>
              <button
                type="submit"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out"
              >
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
            class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
          >
            {{ isSignUp ? 'Sign In' : 'Sign Up' }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios';

import { useToastStore } from '@/stores/toast'; // Adjust the path if necessary
import { useUserStore } from '@/stores/user';
const userStore = useUserStore();
const toastStore = useToastStore();

const isSignUp = ref(false)

const user = reactive({
  username: '',
  nickname: '',
  password1: "",
  password2: "",
  avatar: null,
})

const errors = reactive({
  username: null,
  nickname: null,
  password1: null,
  password2: null,
  avatar: null,
  general: null, // For non-field-specific errors
});


const emit = defineEmits(['auth-success'])

const toggleAuthMode = () => {
  isSignUp.value = !isSignUp.value
}
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    user.avatar = file;
  }
}
const handleAuth = async () => {
  const action = isSignUp.value ? 'signup' : 'signin';

  // Clear previous errors
  Object.keys(errors).forEach((key) => (errors[key] = null));

  if (action === 'signup') {
    if (!user.nickname) errors.nickname = "Your name is missing";
    if (!user.username) errors.username = "Your username is missing";
    if (!user.password1) errors.password1 = "Your password is missing";
    if (!user.password2) errors.password2 = "Confirm your password";
    if (user.password1 !== user.password2)
      errors.password2 = "Passwords do not match";

    if (Object.values(errors).some((error) => error)) {
      return; // Exit if there are errors
    }

    try {
      const formData = new FormData();
      formData.append("username", user.username);
      formData.append("name", user.nickname);
      formData.append("password1", user.password1);
      formData.append("password2", user.password2);
      if (user.avatar) formData.append("avatar", user.avatar);

      const response = await axios.post("/api/account/users/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.status === 201) {
        toastStore.showToast(5000, "The user is registered. Please log in!", "bg-green-500 dark:bg-green-500");

        userStore.setUserInfo(response.data)
        isSignUp.value = false
      } else {
        errors.general = "Something went wrong. Please try again!";
      }
    } catch (error) {
      errors.general = error.response?.data?.message || "An error occurred.";
    }
  } else if (action === 'signin') {
    if (!user.username) errors.username = "Please enter your username";
    if (!user.password1) errors.password1 = "Please enter your password";

    if (Object.values(errors).some((error) => error)) {
      return; // Exit if there are errors
    }

    try {
      const response = await axios.post("/api/account/login/", {
        username: user.username,
        password: user.password1,
      });

      userStore.setToken(response.data)
      axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;

      toastStore.showToast(5000, "You are logged in successfully!", "bg-green-500 dark:bg-green-500");
      if (response.status === 200) {
        userStore.setUserInfo(response.data)
        emit('auth-success')
        const response2 = await axios.get("/api/account/users/me/")
        if(response.status === 200){
          userStore.setUserInfo(response2.data)
        }
      } else {
        errors.general = "Something went wrong. Please try again!";
      }
    } catch (error) {
      errors.general = error.response?.data?.message || "Invalid login credentials";
    }
  }
};

</script>
