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
                  <img loading="lazy" :src="reservation.post.images[0]" :alt="reservation.post.title" class="w-full h-48 object-cover"/>

                </div>
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-center mb-6 text-white">
                  Please describe the issue you want to Report below!
                </DialogTitle>
                <div v-if="isSending" class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div>
                <textarea v-model="reason" placeholder="Seller didn't deliver!" class="w-full bg-gray-100 py-2 px-4 border border-gray-100 dark:border-gray-800 rounded-md focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-800 dark:text-gray-200 dark:focus:ring-gray-600 dark:focus:border-gray-600"/>
                <button @click="sendReport" :class="{ 'bg-red-500 hover:bg-red-700 text-white': reason.length > 0 && !isSending, 'bg-gray-500 hover:bg-gray-700 text-white': reason.length === 0 || isSending}" class="dark:text-white py-2 px-4 rounded-md text-center w-full mt-4">Send Report</button>
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
import {ref} from 'vue';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
const toastStore = useToastStore();
const props = defineProps({
  reservation: {
    type: Object,
    required: true
  }
})
const reason = ref('')
const isSending = ref(false)
const emit = defineEmits(['closeModal', 'setTransaction'])
const sendReport = () => {
  isSending.value = true;
  axios.post(`api/transaction/reservations/${props.reservation.id}/report/`, { reason: reason.value })
  .then(
    response => {
      isSending.value = false;
      setTransaction(response.data);
    }
  )
  .catch(
    error => {
      console.error(error)
      toastStore.showToast(
        5000,
        "Something went wrong. Please try again!",
        "bg-red-300 dark:bg-red-300",
      );
    }
  )
  ;
}
const setTransaction = (data) => {
  emit('setTransaction', data)
}
const closeModal = () => {
  emit('closeModal')
}
</script>
