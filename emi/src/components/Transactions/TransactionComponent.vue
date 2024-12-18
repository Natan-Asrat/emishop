<template>
  <div
   v-if="transaction"
  :class="['rounded-lg shadow-md overflow-hidden', getCardColor(transaction)]">
  <div class="p-4 flex items-start space-x-4">
    <div :class="['p-2 rounded-full', getIconBackground(transaction)]">
      <component :is="getIcon(transaction)" class="h-6 w-6 text-white" />
    </div>
    <div class="flex-grow">
      <h3 v-if="transaction && transaction?.post && transaction?.post?.title" class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ transaction.post.title }}
      </h3>
      <p v-if="transaction && transaction?.created_at" class="text-sm text-gray-600 dark:text-gray-400">
        {{  formatDate(transaction.created_at) }}
      </p>
      <p v-if="transaction && transaction?.coins_spent" class="text-sm font-medium text-gray-900 dark:text-gray-100 mt-1">
        {{  transaction.coins_spent }} coins
      </p>
      <p v-if="getStatusText(transaction)" :class="['text-xs mt-1', getStatusColor(transaction)]">
        {{ getStatusText(transaction) }}
      </p>
    </div>
    <div v-if="transaction?.quantity" class="text-right">
      <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
        Quantity: {{  transaction.quantity }}
      </p>
    </div>
  </div>

  <div
  v-if="showActions(transaction)"
  class="px-4 pb-4 flex justify-end flex-wrap gap-2 items-center"
>
  <button
    v-if="canAccept(transaction)"
    @click="handleAction(transaction, 'accept')"
    :disabled="isLoading"
    class="px-3 py-1 bg-green-500 text-white rounded-full text-sm flex items-center space-x-1"
  >
    <CheckCircle class="h-4 w-4" />
    <span>Accept</span>
  </button>
  <button
    @click="navigateToChat(transaction)"
    :disabled="isLoading"
    class="px-3 py-1 bg-blue-500 text-white rounded-full text-sm flex items-center space-x-1"
  >
    <MessageCircle class="h-4 w-4" />
    <span>Message</span>
  </button>
  <button
    v-if="canDeliver(transaction)"
    @click="handleAction(transaction, 'complete')"
    :disabled="isLoading"
    class="px-3 py-1 bg-purple-500 text-white rounded-full text-sm flex items-center space-x-1"
  >
    <Archive class="h-4 w-4" />
    <span>Deliver</span>
  </button>
  <button
    v-if="canReceive(transaction)"
    @click="handleAction(transaction, 'complete')"
    :disabled="isLoading"
    class="px-3 py-1 bg-green-500 text-white rounded-full text-sm flex items-center space-x-1"
  >
    <span>Received</span>
  </button>
  <button
    v-if="canCancel(transaction)"
    @click="handleAction(transaction, 'cancel')"
    :disabled="isLoading"
    class="px-3 py-1 bg-red-500 text-white rounded-full text-sm flex items-center space-x-1"
  >
    <span>Cancel</span>
  </button>
  <button
    v-if="canReport(transaction)"
    @click="handleAction(transaction, 'report')"
    :disabled="isLoading"
    class="px-3 py-1 bg-yellow-500 text-white rounded-full text-sm flex items-center space-x-1"
  >
    <span>Report</span>
  </button>
</div>
<ReportComponent v-if="showReportDialog" @setTransaction="setTransaction" @closeModal="closeModal" :reservation="transaction"/>

  </div>
</template>
<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';
import { getOtherPartyOfTrasaction } from '@/utils'
import { CheckCircle, XCircle, AlertTriangle, ShoppingCart, MessageCircle, Archive } from 'lucide-vue-next';
import ReportComponent from './ReportComponent.vue';
import { useUserStore } from '@/stores/user';
const userStore = useUserStore();
const emit = defineEmits(['setTransaction'])
const props = defineProps({
  transaction: {
    type: Object,
    required: true
  },
  trueForReservationFalseForOrder: {
    type: Boolean,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})
const router = useRouter();
const showReportDialog = ref(false);
const isLoading = useRef(false);
const closeModal = () => {
  showReportDialog.value = false;
}

const showActions = (transaction) => {
  return (transaction.status === 'pending' && transaction.seller_accepted) || !props.trueForReservationFalseForOrder;
};
const getCardColor = (transaction) => {
  if (transaction.status === 'reported') return 'bg-red-50 dark:bg-red-900/20';
  if (transaction.status === 'cancelled') return 'bg-gray-50 dark:bg-gray-800/50';
  return 'bg-white dark:bg-gray-800';
};
const getIconBackground = (transaction) => {
  if (transaction.status === 'completed') return 'bg-green-500';
  if (transaction.status === 'cancelled') return 'bg-red-500';
  if (transaction.status === 'reported') return 'bg-yellow-500';
  return 'bg-blue-500';
};
const getIcon = (transaction) => {
  if (transaction.status === 'completed') return CheckCircle;
  if (transaction.status === 'cancelled') return XCircle;
  if (transaction.status === 'reported') return AlertTriangle;
  return ShoppingCart;
};

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
const getStatusColor = (transaction) => {
  if (transaction.status === 'completed') return 'text-green-600 dark:text-green-400';
  if (transaction.status === 'cancelled') return 'text-red-600 dark:text-red-400';
  if (transaction.status === 'reported') return 'text-yellow-600 dark:text-yellow-400';
  return 'text-blue-600 dark:text-blue-400';
};
const getStatusText = (transaction) => {
  if (transaction?.status === 'reported') return 'Under Review';
  if (transaction?.status === 'cancelled') {
    return transaction?.cancelled_by?.id === transaction?.buyer?.id
      ? 'You cancelled this reservation'
      : 'Seller cancelled - Coins refunded';
  }
  if (transaction?.status === 'pending') {
    return !props.trueForReservationFalseForOrder ?
    (
    transaction?.seller_accepted
      ? 'Waiting for you to deliver!'
      : 'Waiting for your acceptance')
     : (transaction?.seller_accepted
      ? 'Accepted by seller'
      : 'Waiting for seller acceptance');
  }
  return 'Completed';
};
const toChat = (transaction) => {
  router.push({
    name: 'chat',
    query: {
      username: getOtherPartyOfTrasaction(userStore.user, transaction).username,
      itemId: transaction.id
    }
  });
}
const navigateToChat = (transaction) => {
  
  if(!transaction.seller_accepted){
    handleAction(transaction, 'accept', () => {toChat(transaction)}) 
  }else {
    toChat(transaction)
  }
};

const canReceive = (transaction) => {
  return transaction.status === 'pending' && transaction.seller_accepted && props.trueForReservationFalseForOrder;
};

const canAccept = (transaction) => {
  return transaction.status === 'pending' && !props.trueForReservationFalseForOrder && !transaction.seller_accepted;
}
const canDeliver = (transaction) => {
  return transaction.status === 'pending' && !props.trueForReservationFalseForOrder && transaction.seller_accepted;
}

const canCancel = (transaction) => {
  return transaction.status === 'pending' || (!props.trueForReservationFalseForOrder && (transaction.status === 'accepted' && transaction.status === 'pending'));
};

const canReport = (transaction) => {
  return transaction.status === 'pending' && transaction.seller_accepted && props.trueForReservationFalseForOrder;
};
const handleAction = async (transaction, action, callback = null) => {
  isLoading.value = true;
  try {
    switch (action) {
      case 'accept':
        axios.post(`api/transaction/orders/${transaction.id}/accept/`)
        .then(
          response => {
            setTransaction(response.data);
            if(callback) callback();
          }
        );
        break
      case 'complete':
        if(props.trueForReservationFalseForOrder){
          axios.post(`api/transaction/reservations/${transaction.id}/complete/`)
          .then(
            response => {
              setTransaction(response.data);
            }
          );
        }else{
          axios.post(`api/transaction/orders/${transaction.id}/complete/`)
          .then(
            response => {
              setTransaction(response.data);
            }
          );
        }
        break;
      case 'cancel':
        axios.post(`api/transaction/reservations/${transaction.id}/cancel/`)
        .then(
          response => {
            setTransaction(response.data);
          }
        );
        break;
      case 'report':
        showReportDialog.value = true;
        break;
    }
    isLoading.value = false;
  } catch (error) {
    console.error(`Error performing ${action}:`, error);
    isLoading.value = false;
  }
};
const setTransaction = (data) => {
  emit('setTransaction', data, props.index);
}
</script>
