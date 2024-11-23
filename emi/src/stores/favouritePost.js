import { defineStore } from "pinia";

export const useFavouritesStore = defineStore({
  id: 'favourite_posts',
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
      const exists = this.posts.some(p => p.id === post.id);
      if (!exists) {
        this.posts.push(post);
      }else{
        this.replacePost(post)
      }
    },
    addPosts(posts) {
      posts.forEach(post => this.addPost(post));
    },
    incrementQuantity(index) {
      if (this.posts[index].quantity < this.posts[index].stockLeft) {
        this.posts[index].quantity++;
      }
    },
    decrementQuantity(index) {
      if (this.posts[index].quantity > 1) {
        this.posts[index].quantity--;
      }
    },
    updateProductQuantity(index, quantity) {
      if (quantity >= 1 && quantity <= this.posts[index].stockLeft) {
        this.posts[index].quantity = quantity;
      }
    }

  }
})
