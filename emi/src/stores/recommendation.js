import { defineStore } from "pinia";

export const useRecommendationStore = defineStore({
  id: 'recommendation',
  state: () => ({
    postInteractions: {},
    interactionTimes: {},
    INTERACTION_WEIGHTS: {
      view: 1,
      detailView: 2,
      reserve: 3
    },
    tempEmbeddings: [],
    EMBEDDING_SIZE: 512,
    userEmbedding: new Array(512).fill(0),
    MAX_TRACKED_POSTS: 500,
    TEMP_TRACKED_POSTS: 20,
    lastSavedDate: null,
    visibilityTimes: {},
    topPosts: []
  }),

  actions: {
    updateInteractionTime(postId, time)  {
      if (!this.interactionTimes[postId]) {
        this.interactionTimes[postId] = 0
      }
      this.interactionTimes[postId] += time
    },
    updatePostInteraction (postId, interactionType, quantity = 1) {
      if (!this.postInteractions[postId]) {
        this.postInteractions[postId] = 0
      }
      const interaction = this.INTERACTION_WEIGHTS[interactionType] * quantity
      this.postInteractions[postId] += interaction
    },
    updateMainListAndGenerateEmbedding() {
      const today = new Date().toDateString()
      const mainEmbeddings = JSON.parse(localStorage.getItem('mainEmbeddings') || '[]')
        let updatedEmbeddings = [...mainEmbeddings, ...this.tempEmbeddings]

        if (updatedEmbeddings.length > this.MAX_TRACKED_POSTS) {
          updatedEmbeddings = updatedEmbeddings.slice(-this.MAX_TRACKED_POSTS)
        }
      if (this.lastSavedDate !== today) {


        localStorage.setItem('mainEmbeddings', JSON.stringify(updatedEmbeddings))
        this.lastSavedDate = today


      }
      const newEmbedding = this.performWeightedAveraging(updatedEmbeddings, this.tempEmbeddings.length)
        this.userEmbedding = newEmbedding

        this.saveUserData()
    },
    performWeightedAveraging(embeddings, lengthOfTemp) {
      const newEmbedding = new Array(this.EMBEDDING_SIZE).fill(0)
      let totalWeight = 0
      const k = 0.05;
      const midpoint = Math.max(0, embeddings.length - lengthOfTemp);
      embeddings.forEach((embedding, index) => {
        const weight = 1 / (1 + Math.exp(-k * (index - midpoint)));

        if (typeof embedding === 'string') {
            try {
                embedding = JSON.parse(embedding);
            } catch (error) {
                console.error("Failed to parse embedding as JSON:", error);
                return;
            }
        }
        embedding.forEach((value, i) => {
          newEmbedding[i] += value * weight
        })
        totalWeight += weight
      })

      return newEmbedding.map(value => value / totalWeight)
    },
    saveUserData() {
      localStorage.setItem('userEmbedding', JSON.stringify(this.userEmbedding))
      localStorage.setItem('postInteractions', JSON.stringify(this.postInteractions))
      localStorage.setItem('interactionTimes', JSON.stringify(this.interactionTimes))
      localStorage.setItem('tempEmbeddings', JSON.stringify(this.tempEmbeddings))
      localStorage.setItem('lastSavedDate', this.lastSavedDate)
    },
    saveRecentlyViewed(postId) {
      const maxInteractions = 5;
      const existingInteractions = JSON.parse(localStorage.getItem('recentlyViewed')) || [];

      const existingIndex = existingInteractions.findIndex(id => id === postId);

      if (existingIndex !== -1) {
        existingInteractions.splice(existingIndex, 1);
      }

      existingInteractions.unshift(postId);

      if (existingInteractions.length > maxInteractions) {
        existingInteractions.pop();
      }
      console.log

      localStorage.setItem('recentlyViewed', JSON.stringify(existingInteractions));
    },
    saveTopPostsToRecentlyViewed(topPosts) {
      if(topPosts != null && topPosts.length > 0){
        topPosts.forEach((postId) => {
          this.saveRecentlyViewed(postId);
        });

      }
    },

    updateVisibility(productId, isVisible) {
      if (isVisible) {
          if (!this.visibilityTimes[productId]) {
              this.visibilityTimes[productId] = {
                  startTime: Date.now(),
                  totalVisibleTime: 0,
                  isVisible: true
              };
          } else if (!this.visibilityTimes[productId].isVisible) {
              this.visibilityTimes[productId].startTime = Date.now();
              this.visibilityTimes[productId].isVisible = true;
          }

      } else {
          if (this.visibilityTimes[productId] && this.visibilityTimes[productId].isVisible) {
              const visibleTime = (Date.now() - this.visibilityTimes[productId].startTime) / 1000; 
              this.visibilityTimes[productId].totalVisibleTime += visibleTime;
              this.updateInteractionTime(productId, visibleTime)

              this.updatePostInteraction(productId, 'view')
              this.visibilityTimes[productId].isVisible = false;
          }
      }
    },
    loadUserData() {
      const savedEmbedding = localStorage.getItem('userEmbedding')
      const savedInteractions = localStorage.getItem('postInteractions')
      const savedTimes = localStorage.getItem('interactionTimes')
      const savedTempEmbeddings = localStorage.getItem('tempEmbeddings')
      const savedLastSavedDate = localStorage.getItem('lastSavedDate')

      if (savedEmbedding) this.userEmbedding = JSON.parse(savedEmbedding)
      if (savedInteractions) this.postInteractions = JSON.parse(savedInteractions)
      if (savedTimes) this.interactionTimes = JSON.parse(savedTimes)
      if (savedTempEmbeddings) this.tempEmbeddings = JSON.parse(savedTempEmbeddings)
      if (savedLastSavedDate) this.lastSavedDate = savedLastSavedDate
    },
    saveToTemporaryStore(products) {
      const embeddings = this.topPosts.map(postId =>
        products.find(product => product.id.toString() === postId)?.embedding || []
      )
      this.tempEmbeddings = embeddings
      this.saveUserData()
    },
    calculateTopInteractedPosts() {
      const weightedInteractions = Object.entries(this.postInteractions).map(([postId, interactions]) => {
        const time = this.interactionTimes[postId] || 0
        return [postId, interactions * time]
      })

      return weightedInteractions
        .sort(([, a], [, b]) => a - b)
        .slice(0, this.TEMP_TRACKED_POSTS)
        .map(([postId]) => postId)
    },
    setTopPosts(posts) {
      this.topPosts = posts;
    }
  },

})
