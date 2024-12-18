import axios from "axios";
import { defineStore } from "pinia";

export const useTransactionsStore = defineStore({
  id: 'transactions',
  state: () => ({
    transactions: [],
    orders: [],
    reservationsCount: null,
    ordersCount: null,
    transactionPages: {
      pending: 1,
      completed: 1,
      cancelled: 1
    },
    orderPages: {
      pending: 1,
      completed: 1,
      cancelled: 1
    },
    hasMoreTransactions: {
      pending: true,
      completed: true,
      cancelled: true
    },
    hasMoreOrders: {
      pending: true,
      completed: true,
      cancelled: true
    },
    isLoadingTransactions: false,
    isLoadingOrders: false,
  }),
  actions: {
    addTransaction(transaction) {
      this.updateCounts()
      const index = this.transactions.findIndex(tr => tr.id === transaction.id);
      if (index !== -1) {
        this.transactions[index] = transaction;
      } else {
        this.transactions.push(transaction);
      }

      this.transactions = [...this.transactions];
    },

    addOrder(transaction) {
      this.updateCounts()
      const index = this.orders.findIndex(tr => tr.id === transaction.id);
      if (index !== -1) {
        this.orders[index] = transaction;
      } else {
        this.orders.push(transaction);
      }

      this.orders = [...this.orders];
    },

    addTransactions(transactions, status) {
      this.updateCounts()
      const filteredTransactions = transactions.filter(
        newTrans => !this.transactions.some(existingTrans => existingTrans.id === newTrans.id)
      )
      this.transactions.push(...filteredTransactions)
    },

    addOrders(transactions, status) {
      this.updateCounts()
      const filteredOrders = transactions.filter(
        newOrder => !this.orders.some(existingOrder => existingOrder.id === newOrder.id)
      )
      this.orders.push(...filteredOrders)
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

      this.transactions = [...this.transactions];
    },
    removeOrder(id) {
      this.updateCounts()
      this.orders = this.orders.filter(transaction => transaction.id !== id);

      this.orders = [...this.orders];
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
    },
    resetPagination(type = 'transactions', status = null) {
      if (type === 'transactions') {
        if (status) {
          this.transactionPages[status] = 1
          this.hasMoreTransactions[status] = true
        } else {
          this.transactionPages = { pending: 1, completed: 1, cancelled: 1 }
          this.hasMoreTransactions = { pending: true, completed: true, cancelled: true }
        }
        this.transactions = []
      } else if (type === 'orders') {
        if (status) {
          this.orderPages[status] = 1
          this.hasMoreOrders[status] = true
        } else {
          this.orderPages = { pending: 1, completed: 1, cancelled: 1 }
          this.hasMoreOrders = { pending: true, completed: true, cancelled: true }
        }
        this.orders = []
      }
    },

    incrementPage(type, status) {
      if (type === 'transactions') {
        this.transactionPages[status] += 1
      } else if (type === 'orders') {
        this.orderPages[status] += 1
      }
    },
  }
})
