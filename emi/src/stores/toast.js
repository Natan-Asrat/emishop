import { defineStore } from "pinia";

export const useToastStore = defineStore({
  id: "toast",

  state: () => ({
    ms: 0,
    message: "",
    classes: "",
    isVisible: false,
    title: '',
    type: '',
    avatar: ''
  }),

  actions: {
    showToast(ms, message, classes, type='', avatar='', title='') {
      this.ms = parseInt(ms);
      this.message = message;
      this.classes = `${classes || ""} -translate-y-28`;
      this.isVisible = true;
      this.title = title;
      this.avatar = avatar;
      this.type = type;

      setTimeout(() => {
        this.classes = this.classes.replace(" -translate-y-28", "");
        setTimeout(() => {
          this.isVisible = false;
        }, this.ms);
      }, 500);
    },
  },
});
