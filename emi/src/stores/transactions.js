import { defineStore } from "pinia";

export const useTransactionsStore = defineStore({
  id: 'transactions',
  state: () => ({
    transactions: []
  }),
  actions: {
    addTransaction(transaction) {

    },
    addTransactions(transaction){


    },
    replaceTransactions(transaction) {
      this.transactions = this.transactions.map(
        tr =>
          tr.id === transaction.id ? transaction : tr
      )
    },
    getTransactions() {
      return this.transactions
    }

  }
})
