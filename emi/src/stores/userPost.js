import { defineStore } from "pinia";

export const useUserPostsStore = defineStore({
  id: 'user_posts',
  state: () => ({
    posts: []
  }),
  actions: {
    replacePost(post) {
      const index = this.posts.findIndex(p => p.id === post.id);
      if (index !== -1) {
        this.posts.splice(index, 1, post);
      }
    },
    addPost(post) {
      this.posts.push(post);
    },
    addPosts(p) {
      p.forEach(post => this.addPost(post));
    },
  }
})
