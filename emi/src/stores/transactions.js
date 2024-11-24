import axios from "axios";
import { defineStore } from "pinia";

export const useTransactionsStore = defineStore({
  id: 'transactions',
  state: () => ({
    transactions: [],
    orders: [],
    reservationsCount: null,
    ordersCount: null,
  }),
  actions: {
    addTransaction(transaction) {
      this.updateCounts()
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

    addOrder(transaction) {
      this.updateCounts()
      const index = this.orders.findIndex(tr => tr.id === transaction.id);
      if (index !== -1) {
        // Replace the existing transaction
        this.orders[index] = transaction;
      } else {
        // Add the new transaction
        this.orders.push(transaction);
      }

      // Ensure reactivity by replacing the array reference
      this.orders = [...this.orders];
    },

    addTransactions(transactions) {
      this.updateCounts()
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

    addOrders(transactions) {
      this.updateCounts()
      transactions.map(newTransaction => {
        const existingIndex = this.orders.findIndex(tr => tr.id === newTransaction.id);
        if (existingIndex !== -1) {
          this.orders[existingIndex] = newTransaction; // Replace if exists
        } else {
          this.orders.push(newTransaction); // Add new
        }
        return newTransaction;
      });

      // Replace with a fresh array reference to ensure reactivity
      this.orders = [...this.orders];
    },
    replaceTransactions(transaction) {
      this.updateCounts()
      this.transactions = this.transactions.map(
        tr =>
          tr.id === transaction.id ? transaction : tr
      )
    },
    replaceOrders(transaction) {
      this.updateCounts()
      this.orders = this.orders.map(
        tr =>
          tr.id === transaction.id ? transaction : tr
      )
    },
    changeTransaction(transaction, index) {
      this.updateCounts()
      this.transactions[index] = transaction;
    },
    changeOrder(transaction, index) {
      this.updateCounts()
      this.orders[index] = transaction;
    },
    removeTransaction(id) {
      this.updateCounts()
      this.transactions = this.transactions.filter(transaction => transaction.id !== id);

      // Ensure reactivity by replacing the array reference
      this.transactions = [...this.transactions];
    },
    removeOrder(id) {
      this.updateCounts()
      this.order = this.order.filter(transaction => transaction.id !== id);

      // Ensure reactivity by replacing the array reference
      this.order = [...this.order];
    },
    getTransactions() {
      return this.transactions
    },
    updateCounts(){
      this.updateOrdersCount()
      this.updateReservationCount()
    },
    updateOrdersCount() {
      axios.get('api/transaction/orders/count/')
      .then(
        response => {
          console.log('counts', response.data)
          this.ordersCount = response.data
        }
      )
    },
    updateReservationCount() {
      axios.get('api/transaction/reservations/count/')
      .then(
        response => {
          this.reservationsCount = response.data
        }
      )
    }

  }
})
