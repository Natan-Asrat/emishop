<template>
    <div @click="installPwa" v-if="showPrompt" class="pwa-install-prompt">
      <p>Install this app for a better experience!</p>
      <button >Click here to Install!</button>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        showPrompt: false,
      };
    },
    mounted() {
      window.addEventListener('beforeinstallprompt', (event) => {
        event.preventDefault();
        // Stash the event so it can be triggered later.
        this.deferredPrompt = event;
        // Update UI notify the user they can install the PWA
        this.showPrompt = true;
      });
    },
    methods: {
      installPwa() {
        if (this.deferredPrompt) {
          // Show the install prompt
          this.deferredPrompt.prompt();
          // Wait for the user to respond to the prompt
          this.deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
              console.log('User accepted the A2HS prompt');
            } else {
              console.log('User dismissed the A2HS prompt');
            }
            this.deferredPrompt = null;
            this.showPrompt = false;
          });
        }
      },
    },
  };
  </script>

  <style scoped>
  .pwa-install-prompt {
    background: #f0f0f0;
    padding: 10px;
    text-align: center;
  }
  </style>
