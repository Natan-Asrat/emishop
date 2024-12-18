import { defineStore } from "pinia";

export const useUserPostsStore = defineStore({
  id: 'user_posts',
  state: () => ({
    posts: [],
    page: 1,
    hasMore: true,
    isLoading: false,
  }),
  actions: {
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
    addPost(post) {
      // Only add if not already exists
      if (!this.posts.find(p => p.id === post.id)) {
        this.posts.push(post);
      }
    },
    
    changePost(post, index) {
      this.posts[index] = post;
    },
    addPosts(p) {
      p.forEach(post => this.addPost(post));
    },
    setPosts(posts) {
      this.posts = posts;
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
