import { defineStore } from "pinia";

export const useTransactionsStore = defineStore({
  id: 'transactions',
  state: () => ({
    transactions: []
  }),
  actions: {
    addTransaction(transaction) {
      const index = this.transactions.findIndex(tr => tr.id === transaction.id);
      if (index !== -1) {
        // Replace the existing transaction
        this.transactions[index] = transaction;
      } else {
        // Add the new transaction
        this.transactions.push(transaction);
      }

      // Ensure reactivity by replacing the array reference
      this.transactions = [...this.transactions];
    },

    addTransactions(transactions) {
      transactions.map(newTransaction => {
        const existingIndex = this.transactions.findIndex(tr => tr.id === newTransaction.id);
        if (existingIndex !== -1) {
          this.transactions[existingIndex] = newTransaction; // Replace if exists
        } else {
          this.transactions.push(newTransaction); // Add new
        }
        return newTransaction;
      });

      // Replace with a fresh array reference to ensure reactivity
      this.transactions = [...this.transactions];
    },

    replaceTransactions(transaction) {
      this.transactions = this.transactions.map(
        tr =>
          tr.id === transaction.id ? transaction : tr
      )
    },
    changeTransaction(transaction, index) {
      this.transactions[index] = transaction;
    },
    removeTransaction(id) {
      this.transactions = this.transactions.filter(transaction => transaction.id !== id);

      // Ensure reactivity by replacing the array reference
      this.transactions = [...this.transactions];
    },
    getTransactions() {
      return this.transactions
    }

  }
})
