import { defineStore } from "pinia";

export const useFeedPostStore = defineStore({
  id: 'feed_posts',
  state: () => ({
    posts: [],
    searchResults: [],
    isSearchExpanded: false,
  }),
  actions: {
    setSearchExpanded(expanded) {
      this.isSearchExpanded = expanded;
    },
    toggleSearch() {
      this.isSearchExpanded =!this.isSearchExpanded;
    },
    replacePost(post) {
      const index = this.posts.findIndex(p => p.id === post.id);
      if (index !== -1) {
        this.posts.splice(index, 1, post);
      }else{
        this.addPost(post)
      }
    },
    setSearchresults (results) {
      this.searchResults = results;
    },
    addPost(post) {
      this.posts.push(post);
    },
    addPosts(p) {
      p.forEach(post => this.addPost(post));
    },
    getPosts() {
      return this.posts;
    },
    changePost(post, index) {
      this.posts[index] = post;
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
    },

  }
})
