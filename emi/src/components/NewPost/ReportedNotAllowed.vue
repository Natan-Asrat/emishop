<template>
  <TransitionRoot appear :show="true" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25 backdrop-blur-sm" />
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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-900 p-6 text-left align-middle shadow-xl transition-all">
              <div class="flex flex-col items-center">
                <!-- <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div> -->
                <div v-if="reservation.post" class="mb-5">
                  <img :src="reservation.post.images[0]" :alt="reservation.post.title" class="w-full h-48 object-cover"/>

                </div>
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-white text-center">
                  You are not allowed to make a post for 30 days.
                </DialogTitle>
                <p class="mt-2 text-sm text-gray-400 text-center">
                  You have been reported on by user '{{ reservation.buyer.username }}' for reason '{{ reservation.report_reason }}'' on item '{{ reservation.post.title }}' <span v-if="reservation.reported_at_formatted">at {{ reservation.reported_at_formatted }}</span>
                </p>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
defineProps({
  reservation: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['closeModal'])
const closeModal = () => {
  emit('closeModal')
}
</script>
