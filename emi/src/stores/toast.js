import { defineStore } from "pinia";

export const useToastStore = defineStore({
  id: "toast",

  state: () => ({
    ms: 0,
    message: "",
    classes: "",
    isVisible: false,
  }),

  actions: {
    showToast(ms, message, classes) {
      console.log("showing toast", message);
      this.ms = parseInt(ms);
      this.message = message;
      this.classes = `${classes || ""} -translate-y-28`;
      this.isVisible = true;

      // Hide toast after duration
      setTimeout(() => {
        this.classes = this.classes.replace(" -translate-y-28", "");
        setTimeout(() => {
          this.isVisible = false;
        }, this.ms); // Match the CSS transition duration
      }, 500);
    },
  },
});
