<template>
  <nav ref="navbarRef" class="w-full
    z-20 top-0 left-0 fixed

    border-b
    transition-transform duration-300" :style="{ transform: `translateY(${navbarTransform})` }">
     <slot />
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, defineEmits } from 'vue';
const emit = defineEmits(['reachedLastElement']);
const navbarTransform = ref('0');
const navbarRef = ref<HTMLElement>();


let lastScroll = 0;
let isScrollingDown = false;

const handleScroll = () => {
    const navbarH = navbarRef.value?.clientHeight as number;
    const currentScroll = window.scrollY;

    if (currentScroll > lastScroll && !isScrollingDown) {
        isScrollingDown = true;
        navbarTransform.value = `-${navbarH}px`;
    } else if (currentScroll < lastScroll && isScrollingDown) {
        isScrollingDown = false;
        navbarTransform.value = '0';
    }

    lastScroll = currentScroll <= 0 ? 0 : currentScroll;

    if ((document.documentElement.scrollHeight - window.scrollY) === window.innerHeight) {
        emit('reachedLastElement');
    }
};

onMounted(() => {
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});
</script>
