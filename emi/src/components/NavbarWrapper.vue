<template>
  <nav ref="navbarRef" class="w-full bg-slate-950
    z-20 top-0 left-0 fixed
    border-b
    transition-transform duration-300" :style="{ transform: `translateY(${navbarTransform})` }">
     <slot />
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';

const navbarTransform = ref('0');
const navbarRef = ref<HTMLElement>();


let lastScroll = 0;
let isScrollingDown = false;

// Start calculating scroll direction and apply translateY
const handleScroll = () => {
    const navbarH = navbarRef.value?.clientHeight as number;
    const currentScroll = window.scrollY;

    if (currentScroll > lastScroll && !isScrollingDown) {
        // scrolling down
        isScrollingDown = true;
        navbarTransform.value = `-${navbarH}px`;  // Hide the navbar
    } else if (currentScroll < lastScroll && isScrollingDown) {
        // scrolling up
        isScrollingDown = false;
        navbarTransform.value = '0';  // Show the navbar
    }

    lastScroll = currentScroll <= 0 ? 0 : currentScroll; // Prevent negative scroll values
};

onMounted(() => {
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});
</script>
