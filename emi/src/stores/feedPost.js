import { defineStore } from "pinia";

export const useFeedPostStore = defineStore({
  id: 'feed_posts',
  state: () => ({
    posts: [],
    searchResults: [],
    isSearchExpanded: false,
    page: 1,
    hasMore: true,
    isLoading: false,
    searchPage: 0,
    hasMoreSearchResults: true
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
      const updatedPost = {
        ...post,
        liked: post.setLiked ? post.liked : this.posts[index].liked
      };
      if (index !== -1) {
        this.posts.splice(index, 1, updatedPost);
      }
    },
    setSearchresults (results) {
      this.searchResults.push(...results);
      
    },
    addPost(post) {
      const exists = this.posts.some(p => p.id === post.id);
      if (!exists) {
        this.posts.push(post);
      }
    },
    addPosts(posts) {
      const newPosts = [];
      posts.forEach(post => {
        const exists = this.posts.some(p => p.id === post.id);
        if (!exists) {
          newPosts.push(post);
        }
      });
      this.posts = [...this.posts, ...newPosts];
    },
    setPosts(posts) {
      this.posts = posts;
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
    resetPagination() {
      this.page = 1;
      this.hasMore = true;
      this.posts = [];
    },
    incrementPage() {
      this.page += 1;
    },
  }
})
