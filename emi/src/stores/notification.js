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
      this.notifications= notifications
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
      notifications.map(newNotification => {
        const existingIndex = this.notifications.findIndex(nt => nt.id === newNotification.id);
        if (existingIndex !== -1) {
          this.notifications[existingIndex] = newNotification; // Replace if exists
        } else {
          this.notifications.push(newNotification); // Add new
        }
        return newNotification;
      });

      // Replace with a fresh array reference to ensure reactivity
      this.notifications = [...this.notifications];
      this.sort()
      this.updateGroupedNotifications()
      this.updateCounts()
    },
    sort () {
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
      console.log("grouped", this.groupedNotifications)

    },

    updateCounts() {
      axios.get('api/notification/notifications/count/')
      .then(
        response => {
          console.log("count", response.data)
          this.count = response.data
        }
      )
    }

  }
})
