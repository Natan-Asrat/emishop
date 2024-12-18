<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <div class="flex">
      <h1 v-if="trueForReservationFalseForOrder" class="text-2xl flex-grow font-bold text-gray-900 dark:text-gray-100 mb-6">Reservations</h1>
      <h1 v-else class="text-2xl flex-grow font-bold text-gray-900 dark:text-gray-100 mb-6">Orders</h1>
      <router-link
        :to="{'name': 'notifications'}"
        class="p-2 mr-2 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        aria-label="Notifications"
      >
        <BellIcon class="h-6 w-6" />
      </router-link>
      <div
      @click="trueForReservationFalseForOrder=!trueForReservationFalseForOrder"
      class="flex rounded-lg h-8 py-auto px-5 text-sm font-medium leading-5 ring-white ring-opacity-60 ring-offset-2 focus:outline-none ring-2 bg-white dark:bg-gray-700 shadow text-blue-700 dark:text-blue-200"
      :class="{
        ' ring-offset-blue-400': trueForReservationFalseForOrder,
        ' ring-offset-green-400': !trueForReservationFalseForOrder
      }">
        <span class="dark:text-gray-100 text-gray-900 inline-flex items-center mr-3">
          <span v-if="!trueForReservationFalseForOrder">
            <span v-if="transactionStore.reservationsCount != null" class="inline-block rounded-full bg-gray-500 w-5 h-5 text-center mr-2 text-white  dark:text-black" :class="{'bg-red-500': transactionStore.reservationsCount.pending > 0}">
              {{ transactionStore.reservationsCount.pending }}
            </span> Reservations</span>
            <span v-else>
              <span v-if="transactionStore.ordersCount != null" class="inline-block rounded-full bg-gray-500 w-5 h-5 text-center mr-2 text-white  dark:text-black" :class="{'bg-green-500': transactionStore.ordersCount.pending > 0}">
                {{ transactionStore.ordersCount.pending }}
              </span>
              Orders
            </span>
            </span>
        <div class="flex flex-col">

          <ArrowLeft
          class="w-4 h-4"
          style="margin-top: 3px"
          :class="{
            'dark:text-white text-gray-900': !trueForReservationFalseForOrder,
            'darK:text-green-600 text-green-600': trueForReservationFalseForOrder
          }"/>
          <ArrowRight
          class="w-4 h-4"
          style="margin-top: -3px"
          :class="{
            'dark:text-white text-gray-900': trueForReservationFalseForOrder,
            'darK:text-red-600 text-red-600': !trueForReservationFalseForOrder
          }"/>
        </div>
      </div>
    </div>
    <div v-if="isLoading" class='mb-5 text-center dark:text-gray-100'>Loading...</div>
  <TabsComponent :trueForReservationFalseForOrder="trueForReservationFalseForOrder" @setCurrentTab="setCurrentTab" :currentTab="currentTab"/>
    <div class="space-y-4 mb-16">
      <TransactionComponent 
        :trueForReservationFalseForOrder="trueForReservationFalseForOrder" 
        @setLoading="transactionStore.isLoadingTransactions = $event"
        @removeTransaction="removeTransaction" 
        @setTransaction="handleSetTransaction" 
        v-for="(transaction, index) in filteredTransactions" 
        :key="transaction.id" 
        :index="index" 
        :transaction="transaction" 
      />
    </div>
    <SpinnerComponent v-if="transactionStore.isLoadingTransactions || transactionStore.isLoadingOrders"/>
    <div class="text-center dark:text-gray-100" v-if="!filteredTransactions || filteredTransactions.length === 0">
      You don't have any transactions yet.
    </div>
    <FooterComponent />
  </div>
</template>
<script>
import TabsComponent from '@/components/Transactions/TabsComponent.vue';
import TransactionComponent from '@/components/Transactions/TransactionComponent.vue';
import { useTransactionsStore } from '@/stores/transactions';
import FooterComponent from '@/components/FooterComponent.vue';
import axios from 'axios';
import { ArrowLeft, ArrowRight, BellIcon } from 'lucide-vue-next';
import SpinnerComponent from '@/components/SpinnerComponent.vue';
export default {
  components: {
    TabsComponent,
    TransactionComponent,
    FooterComponent,
    ArrowLeft,
    ArrowRight,
    BellIcon,
    SpinnerComponent
  },
  setup() {
    const transactionStore = useTransactionsStore();
    return {
      transactionStore,
    }
  },
  computed: {
    filteredTransactions() {
      const filtered = this.trueForReservationFalseForOrder ? this.transactionStore.transactions.filter(
        t => {
          if (this.currentTab === 'Pending') return t.status === 'pending';
          if (this.currentTab === 'Completed') return t.status === 'completed';
          if (this.currentTab === 'Cancelled') return t.status === 'cancelled';
          return false;
    }) : this.transactionStore.orders.filter(
        t => {
          if (this.currentTab === 'Pending') return t.status === 'pending';
          if (this.currentTab === 'Completed') return t.status === 'completed';
          if (this.currentTab === 'Cancelled') return t.status === 'cancelled';
          return false;
    })
    return filtered;
    }
  },
  data() {
    return {
      currentTab: 'Pending',
      isLoading: false,
      trueForReservationFalseForOrder: true
    }
  },
  methods: {
    setCurrentTab(tab) {
      this.currentTab = tab
    },
    handleSetTransaction(transaction, index) {
      if(this.trueForReservationFalseForOrder){
        this.transactionStore.changeTransaction(transaction, index);
      }else{
        this.transactionStore.changeOrder(transaction, index);
      }
    },
    removeTransaction(id) {
      if(this.trueForReservationFalseForOrder){
        this.transactionStore.removeTransaction(id);
      }else{
        this.transactionStore.removeOrder(id);
      }
    },
    async fetchTransactions() {
      const status = this.currentTab.toLowerCase()
      if (this.transactionStore.isLoadingTransactions || 
          !this.transactionStore.hasMoreTransactions[status]) return

      this.transactionStore.isLoadingTransactions = true
      try {
        const response = await axios.get('api/transaction/reservations/', {
          params: { 
            page: this.transactionStore.transactionPages[status],
            status: status
          }
        })

        const newTransactions = response.data.results

        this.transactionStore.addTransactions(newTransactions, status)

        this.transactionStore.hasMoreTransactions[status] = response.data.next !== null
        
        if (this.transactionStore.hasMoreTransactions[status]) {
          this.transactionStore.incrementPage('transactions', status)
        }
      } catch (error) {
        console.error('Error fetching transactions:', error)
      } finally {
        this.transactionStore.isLoadingTransactions = false
      }
    },

    async fetchOrders() {
      const status = this.currentTab.toLowerCase()
      if (this.transactionStore.isLoadingOrders || 
          !this.transactionStore.hasMoreOrders[status]) return

      this.transactionStore.isLoadingOrders = true
      try {
        const response = await axios.get('api/transaction/orders/', {
          params: { 
            page: this.transactionStore.orderPages[status],
            status: status
          }
        })

        const newOrders = response.data.results

        this.transactionStore.addOrders(newOrders, status)

        this.transactionStore.hasMoreOrders[status] = response.data.next !== null
        
        if (this.transactionStore.hasMoreOrders[status]) {
          this.transactionStore.incrementPage('orders', status)
        }
      } catch (error) {
        console.error('Error fetching orders:', error)
      } finally {
        this.transactionStore.isLoadingOrders = false
      }
    },

    handleScroll() {
      const scrolledToBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 100
      if (scrolledToBottom) {
        if (this.trueForReservationFalseForOrder) {
          this.fetchTransactions()
        } else {
          this.fetchOrders()
        }
      }
    }
  },

  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },

  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },

  watch: {
    currentTab: {
      handler(newTab) {
        const status = newTab.toLowerCase()
        const type = this.trueForReservationFalseForOrder ? 'transactions' : 'orders'
        
        this.transactionStore.resetPagination(type, status)
        
        if(this.trueForReservationFalseForOrder){
          this.fetchTransactions()
        }else{
          this.fetchOrders()
        }
      },
      immediate: true,
    },

    trueForReservationFalseForOrder: {
      handler(newTab) {
        const status = this.currentTab.toLowerCase()
        const type = this.trueForReservationFalseForOrder ? 'transactions' : 'orders'
        
        this.transactionStore.resetPagination(type, status)
        
        if(this.trueForReservationFalseForOrder){
          this.fetchTransactions()
        }else{
          this.fetchOrders()
        }
      },
      immediate: true,
    }
  }
}
</script>
