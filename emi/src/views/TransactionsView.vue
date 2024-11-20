<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Transactions</h1>
    <div v-if="isLoading" class='mb-5 text-center dark:text-gray-100'>Loading...</div>
  <TabsComponent @setCurrentTab="setCurrentTab" :currentTab="currentTab"/>
    <div class="space-y-4 mb-16">
      <TransactionComponent @removeTransaction="removeTransaction" @setTransaction="handleSetTransaction" v-for="(transaction, index) in filteredTransactions" :key="transaction.id" :index="index" :transaction="transaction" />
    </div>
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
export default {
  components: {
    TabsComponent,
    TransactionComponent,
    FooterComponent
  },
  setup() {
    const transactionStore = useTransactionsStore();
    return {
      transactionStore,
    }
  },
  computed: {
    filteredTransactions() {
      const filtered = this.transactionStore.transactions.filter(
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
      isLoading: false
    }
  },
  methods: {
    setCurrentTab(tab) {
      this.currentTab = tab
    },
    handleSetTransaction(transaction, index) {
      this.transactionStore.changeTransaction(transaction, index);
    },
    removeTransaction(id) {
      this.transactionStore.removeTransaction(id);
    },
    fetchTransactions() {
      this.isLoading = true;
      axios.get(`/api/transaction/reservations/?status=${this.currentTab.toLowerCase()}`)
      .then(
        response => {
          console.log(response.data)
          this.transactionStore.addTransactions(response.data);
          this.isLoading = false;
        }
      )
    }
  },
  watch: {
    currentTab: {
      handler(newTab) {
        console.log(newTab);
        console.log("tra", this.transactionStore.transactions);
        this.fetchTransactions();
      },
      immediate: true,
    }

  }
}
</script>
