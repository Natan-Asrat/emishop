<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="max-w-3xl mx-auto">
      <div class="min-h-screen py-4 px-5 rounded-lg shadow-lg flex flex-col">
        <div class="flex flex-col bg-white h-full dark:bg-gray-800 flex-grow">
          <HeaderComponent :recipientName="recipientName" />
          <ReservationPreview v-if="reservation" :reservation="reservation"/>
          <div class="flex-grow overflow-y-auto h-96 p-4" ref="messagesContainer">
            <ChatMessage
              v-for="message in sortedMessages"
              :key="message.id"
              :message="message"
              :isOwn="message.sender.id === userStore.user.id"
            />
          </div>
          <div class="border-t dark:border-gray-700 p-4">
            <div class="flex space-x-2">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type your message..."
                class="flex-1 rounded-lg border dark:text-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                @keyup.enter="sendMessage"
              />
              <button
                @click="sendMessage"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <SpinnerComponent v-if="isLoadingMessages" />
</template>
<script>
import SpinnerComponent from '@/components/SpinnerComponent.vue';
import HeaderComponent from '@/components/Chat/HeaderComponent.vue';
import ReservationPreview from '@/components/Chat/ReservationPreview.vue';
import axios from 'axios'
import { WS_BASE_URL } from '@/config';
import { useUserStore } from '@/stores/user';
import ChatMessage from '@/components/Chat/ChatMessage.vue';
import { useToastStore } from '@/stores/toast';
import { nextTick } from 'vue';
export default {
  components: {
    HeaderComponent,
    SpinnerComponent,
    ReservationPreview,
    ChatMessage
  },
  data() {
    return {
      messages: [],
      ws: null,
      conversation: null,
      newMessage: '',
      reservation: null,
      recipientName: this.$route.query.username,
      page: 0,
      hasMoreMessages: true,
      isLoadingMessages: false,
    }
  },
  computed: {
    sortedMessages() {
      return [...this.messages].sort((a, b) => {
        // Precisely compare timestamps including microseconds
        return new Date(a.sent_at).getTime() - new Date(b.sent_at).getTime();
      });
    }
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore
    }
  },
  mounted() {
    const itemId = this.$route.query.itemId;
    if(itemId) {
      this.fetchConversation(itemId)
    }else{
      console.error("no item id", itemId)
    }
    if (this.$refs.messagesContainer) {
      this.$refs.messagesContainer.addEventListener('scroll', this.handleScroll);
    }
  },
  beforeUnmount() {
    // Remove scroll event listener to prevent memory leaks
    if (this.$refs.messagesContainer) {
      this.$refs.messagesContainer.removeEventListener('scroll', this.handleScroll);
    }
  },

  methods: {
    handleScroll() {
      const container = this.$refs.messagesContainer;
      // Check if scrolled to the top
      if (container.scrollTop === 0 && this.hasMoreMessages && !this.isLoadingMessages) {
        this.fetchMessages();
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
          });
        }
      });
    },
    fetchConversation(itemId) {
      axios.get(`api/transaction/reservations/${itemId}/conversation`)
      .then(
        response => {
          this.conversation = response.data.conversation;
          this.reservation = response.data.reservation;
          this.page = 0;
          this.messages = [];
          this.hasMoreMessages = true;
        
          this.fetchMessages()
          this.establishWebsocket()
        }
      )

    },
    fetchMessages() {
      if (this.isLoadingMessages || !this.conversation) return;
      this.isLoadingMessages = true;
      this.page ++;

      axios.get(`api/notification/conversations/${this.conversation.id}/messages`, {
        params: {
          page: this.page,
          page_size: 20
        }
      })
      .then(
        response => {
          const data = response.data;
          const previousHeight = this.$refs.messagesContainer.scrollHeight;
          this.messages = [...this.messages, ...(data.results)];
          this.hasMoreMessages = data.next !== null;
          this.isLoadingMessages = false;
          nextTick(() => {
            
            if(this.page === 1) {
              this.scrollToBottom();
            }else{
              const newHeight = this.$refs.messagesContainer.scrollHeight;
              const diff = newHeight - previousHeight;
              this.$refs.messagesContainer.scrollTop += diff;
            }
          })

        }
      )
    },
    establishWebsocket() {
      this.ws = new WebSocket(`${WS_BASE_URL}/ws/chat/${this.conversation.id}?token=${this.userStore.user.access}`)
      this.ws.onopen = () => {
        console.log(`WebSocket connection established`);
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.messages = [...this.messages, data.object];
        this.scrollToBottom();

      };

      this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
          toastStore.showToast(
            5000,
            "WebSocket connection error. Please refresh!",
            "bg-red-300 dark:bg-red-300",
          );
        };

      this.ws.onclose = () => {
        console.error(`WebSocket connection closed`);
      };
    },
    sendMessage () {
      if (!this.newMessage.trim()) return;
      const messageData = {
        type: 'chat_message',
        message: this.newMessage,
        sender_id: this.userStore.user,
        recipient_id: this.$route.query.username,
        reservation_id: this.$route.query.itemId
      }; // Send via WebSocket
      this.ws.send(JSON.stringify(messageData));
      this.newMessage = '';
    }
  }
}
</script>
