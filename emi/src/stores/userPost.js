import { defineStore } from "pinia";

export const useUserPostsStore = defineStore({
  id: 'user_posts',
  state: () => ({
    posts: []
  }),
  actions: {
    replacePost(post) {

    },
    addPost(post) {

    },
    addPosts(posts){

    },
    getPosts(post) {

    }
  }
})
