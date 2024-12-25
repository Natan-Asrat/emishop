<script setup>
import { useToastStore } from "@/stores/toast";
const store = useToastStore();
</script>

<template>
  <div
    v-if="store.isVisible"
    :class="store.classes"
    class="transition ease-in-out shadow-lg delay-2000 duration-2000 px-6 py-3 fixed top-4 right-1/2 translate-x-1/2 rounded-lg z-[9999]"
  >
  <div v-if="store.type == 'message'" class="flex gap-4">
    <img class="w-12 h-12 rounded-full object-cover" :src="store.avatar" alt="avatar"> 
    <div>
      <h2 class="font-bold max-w-[90px] truncate">{{store.title}}</h2>
      <p class="ml-2 max-w-[90px] truncate">    {{ store.message }}    </p>

    </div>

  </div>
  <div v-else>
    {{ store.message }}

  </div>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 2s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}

.toast-enter-to,
.toast-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.toast-move {
  transition: transform 2s ease;
}
</style>
