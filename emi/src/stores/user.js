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
    async initStore() {

      if (localStorage.getItem("user.access")) {

        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.name = localStorage.getItem("user.name");
        this.user.username = localStorage.getItem("user.username");
        this.user.avatar = localStorage.getItem("user.avatar");
      localStorage.setItem("user.avatar", this.user.avatar);
        this.user.isAuthenticated = true;

        await this.refreshToken();
        await this.refreshCoins();
      }
    },
    async refreshCoins() {
      const response = await axios.get(`api/account/users/me/`)
      this.setUserInfo(response.data)
      this.user.coins = response.data.coins;

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
      this.user.avatar = null;

      localStorage.setItem("user.access", "");
      localStorage.setItem("user.refresh", "");
      localStorage.setItem("user.id", "");
      localStorage.setItem("user.name", "");
      localStorage.setItem("user.username", "");
      localStorage.setItem("user.avatar", "");
    },

    setUserInfo(user) {
      console.log("setting user")
      this.user.id = user.id;
      this.user.name = user.name;
      this.user.username = user.username;
      this.user.avatar = user.avatar;
      this.user.coins = user.coins;
      localStorage.setItem("user.id", this.user.id);
      localStorage.setItem("user.name", this.user.name);
      localStorage.setItem("user.username", this.user.username);
      localStorage.setItem("user.avatar", this.user.avatar);
      console.log("set", localStorage.getItem("user.id"))

    },

    async refreshToken() {
      try{
        const response = await axios
          .post("/api/account/refresh/", {
            refresh: this.user.refresh,
          })
        if(response) {
            this.user.access = response.data.access;

            localStorage.setItem("user.access", response.data.access);

            axios.defaults.headers.common["Authorization"] =
              "Bearer " + response.data.access;
        }else{
          this.removeToken();
        }

      }catch(error){
          console.log(error);

          this.removeToken();
        }
    },
  },
});
