<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Transactions</h1>
    <TabsComponent @setCurrentTab="setCurrentTab" :currentTab="currentTab"/>
    <div class="space-y-4">
      <TransactionComponent @setTransaction="handleSetTransaction" v-for="(transaction, index) in filteredTransactions" :key="transaction.id" :index="index" :transaction="transaction" />
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
  data() {
    return {
      currentTab: '',
      transactions: []
    }
  },
  methods: {
    setCurrentTab(tab) {
      this.currentTab = tab
    },
    handleSetTransaction(transaction, index) {
      this.transactions[index] = transaction;
    },
  }
}
</script>
