<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="max-w-3xl mx-auto">
      <div class="min-h-screen p-4 rounded-lg shadow-lg flex flex-col">
        <div class="flex flex-col bg-white h-full dark:bg-gray-800 flex-grow">
          <HeaderComponent :recipientName="''" />
          <ReservationPreview v-if="reservation" :reservation="reservation"/>
          <div class="flex-grow overflow-y-auto h-96 p-4" ref="messagesContainer">
            <ChatMessage
              v-for="message in messages"
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
</template>
<script>
import HeaderComponent from '@/components/Chat/HeaderComponent.vue';
import ReservationPreview from '@/components/Chat/ReservationPreview.vue';
import axios from 'axios'
import { WS_BASE_URL } from '@/config';
import { useUserStore } from '@/stores/user';
import ChatMessage from '@/components/Chat/ChatMessage.vue';
export default {
  components: {
    HeaderComponent,
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
    }
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    }
  },
  mounted() {
    this.scrollToBottom();
    const itemId = this.$route.query.itemId;
    if(itemId) {
      console.log("item id", itemId)
      this.fetchConversation(itemId)
    }else{
      console.log("no item id")
    }
  },
  watch: {
    messages() {
      this.scrollToBottom();
    },
  },
  methods: {
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
          this.fetchMessages()
          console.log("establishing")
          this.establishWebsocket()
        }
      )

    },
    fetchMessages() {
      axios.get(`api/notification/conversations/${this.conversation.id}/messages`)
      .then(
        response => {
          const data = response.data;
          this.messages.push(...data);
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
        this.messages.push(data.object);
      };

      this.ws.onclose = () => {
        console.log(`WebSocket connection closed`);
      };
    },
    sendMessage () {
      if (!this.newMessage.trim()) return;
      const messageData = {
        type: 'chat_message',
        message: this.newMessage,
        sender_id: this.userStore.user,
        recipient_id: this.$route.query.username
      }; // Send via WebSocket
      this.ws.send(JSON.stringify(messageData));
      this.newMessage = '';
    }
  }
}
</script>
