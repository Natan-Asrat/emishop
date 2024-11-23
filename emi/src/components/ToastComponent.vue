<script setup>
import { useToastStore } from "@/stores/toast";
const store = useToastStore();
</script>
<template>
  <div
    v-if="store.isVisible"
    :class="store.classes"
    class="transition ease-in-out shadow-xl delay-500 duration-500 px-6 py-3 fixed top-full right-8 rounded-lg"
  >
    {{ store.message }}
  </div>
</template>
