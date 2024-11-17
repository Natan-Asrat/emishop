import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      name: null,
      username: null,
      access: null,
      refresh: null,
      coins: 0,
    },
  }),

  actions: {
    initStore() {

      if (localStorage.getItem("user.access")) {

        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.name = localStorage.getItem("user.name");
        this.user.username = localStorage.getItem("user.username");
        this.user.avatar = localStorage.getItem("user.avatar");
        this.user.isAuthenticated = true;

        this.refreshToken();

      }
    },

    setToken(data) {

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);

    },

    removeToken() {

      this.user.refresh = null;
      this.user.access = null;
      this.user.isAuthenticated = false;
      this.user.id = false;
      this.user.name = false;
      this.user.username = false;

      localStorage.setItem("user.access", "");
      localStorage.setItem("user.refresh", "");
      localStorage.setItem("user.id", "");
      localStorage.setItem("user.name", "");
      localStorage.setItem("user.username", "");
    },

    setUserInfo(user) {

      this.user.id = user.id;
      this.user.name = user.name;
      this.user.username = user.username;
      this.user.avatar = user.avatar;
      this.user.coins = user.coins;
      localStorage.setItem("user.id", this.user.id);
      localStorage.setItem("user.name", this.user.name);
      localStorage.setItem("user.username", this.user.username);
      localStorage.setItem("user.avatar", this.user.avatar);

    },

    refreshToken() {
      axios
        .post("/api/account/refresh/", {
          refresh: this.user.refresh,
        })
        .then((response) => {
          this.user.access = response.data.access;

          localStorage.setItem("user.access", response.data.access);

          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          console.log(error);

          this.removeToken();
        });
    },
  },
});
