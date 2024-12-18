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
      this.ms = parseInt(ms);
      this.message = message;
      this.classes = `${classes || ""} -translate-y-28`;
      this.isVisible = true;

      setTimeout(() => {
        this.classes = this.classes.replace(" -translate-y-28", "");
        setTimeout(() => {
          this.isVisible = false;
        }, this.ms);
      }, 500);
    },
  },
});
