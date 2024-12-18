import { defineStore } from "pinia";
import axios from "axios";

export const useNotificationStore = defineStore({
  id: 'notification',
  state: () => ({
    notifications: [],
    groupedNotifications: [],
    count: null,
  }),
  actions: {
    setNotifications(notifications) {
      this.notifications = notifications
      this.sort()
      this.updateGroupedNotifications()
      this.updateCounts()
    },
    addNotification(notification) {
      this.notifications.unshift(notification)
      this.sort()
      this.updateGroupedNotifications()
      this.updateCounts()
    },
    addNotifications(notifications) {
      const newNotifications = this.notifications.slice();
      notifications.forEach(newNotification => {
        const existingIndex = newNotifications.findIndex(nt => nt.id === newNotification.id);
        if (existingIndex !== -1) {
          newNotifications[existingIndex] = newNotification; // Replace if exists
        } else {
          newNotifications.push(newNotification); // Add new
        }
      });

      // Replace with a fresh array reference to ensure reactivity
      this.notifications = newNotifications;
      this.sort()
      this.updateGroupedNotifications()
      this.updateCounts()
    },
    sort() {
      this.notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    },
    getTimeLabel(date) {
      const now = new Date();
      const created = new Date(date);

      const differenceInMs = now - created;
      const differenceInDays = Math.floor(differenceInMs / (1000 * 60 * 60 * 24));

      if (differenceInDays === 0) return "Today";
      if (differenceInDays === 1) return "Yesterday";
      if (differenceInDays <= 6) return `${differenceInDays} days ago`;
      if (differenceInDays <= 13) return "A week ago";
      if (differenceInDays <= 30) return `${Math.floor(differenceInDays / 7)} weeks ago`;
      if (differenceInDays <= 365) return `${Math.floor(differenceInDays / 30)} months ago`;
      return "A year ago";
    },

    // Group notifications by time label
    updateGroupedNotifications() {
      this.groupedNotifications = this.notifications.reduce((result, notification) => {
        const label = this.getTimeLabel(notification.created_at); // Get the time label
        let group = result.find((g) => g.date === label); // Check if the group already exists

        if (!group) {
          group = { date: label, notifications: [] }; // Create new group
          result.push(group);
        }

        group.notifications.push(notification); // Add notification to the group
        group.notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // Sort latest first

        return result;
      }, [])

    },

    updateCounts() {
      axios.get('api/notification/notifications/count/')
        .then(
          response => {
            this.count = response.data
          }
        )
    }

  }
})
