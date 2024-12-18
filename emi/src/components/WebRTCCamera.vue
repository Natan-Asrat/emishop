<template>
  <div class="webrtc-camera-container fixed inset-0 z-[9999] bg-black bg-opacity-90 flex items-center justify-center">
    <div class="camera-wrapper w-full max-w-md aspect-square relative">
      <div v-if="!imageCapture" class="camera-preview">
        <video 
          ref="videoElement" 
          autoplay 
          class="w-full h-full object-cover rounded-lg"
        ></video>
        <div class="camera-controls absolute bottom-4 left-0 right-0 flex justify-center space-x-4">
          <button 
            @click="captureImage" 
            class="bg-blue-500 text-white p-3 rounded-full hover:bg-blue-600 transition-colors"
          >
            <Camera class="h-6 w-6" />
          </button>
          <button 
            @click="switchCamera" 
            class="bg-gray-500 text-white p-3 rounded-full hover:bg-gray-600 transition-colors"
          >
            <RefreshCw class="h-6 w-6" />
          </button>
          <button 
            @click="cancelCapture" 
            class="bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition-colors"
          >
            <X class="h-6 w-6" />
          </button>
        </div>
      </div>
      
      <div v-else class="image-preview">
        <img loading="lazy" 
          :src="imageCapture" 
          class="w-full h-full object-cover rounded-lg"
        />
        <div class="image-controls absolute bottom-4 left-0 right-0 flex justify-center space-x-4">
          <button 
            @click="retakePhoto" 
            class="bg-gray-500 text-white p-3 rounded-full hover:bg-gray-600 transition-colors"
          >
            <RotateCcw class="h-6 w-6" />
          </button>
          <button 
            @click="confirmImage" 
            class="bg-green-500 text-white p-3 rounded-full hover:bg-green-600 transition-colors"
          >
            <Check class="h-6 w-6" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Camera, RefreshCw, RotateCcw, Check, X } from 'lucide-vue-next'

const props = defineProps({
  maxWidth: {
    type: Number,
    default: 800
  }
})

const emit = defineEmits(['image-captured', 'image-confirmed', 'close'])

const videoElement = ref(null)
const imageCapture = ref(null)
const currentStream = ref(null)
const currentCameraIndex = ref(0)
const availableCameras = ref([])

const constraints = {
  video: { 
    width: { ideal: props.maxWidth },
    facingMode: 'environment'
  }
}

onMounted(async () => {
  try {
    await initCamera()
  } catch (error) {
    console.error('Error initializing camera:', error)
  }
})

onUnmounted(() => {
  stopCamera()
})

async function initCamera() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    availableCameras.value = devices.filter(device => device.kind === 'videoinput')

    const stream = await navigator.mediaDevices.getUserMedia(constraints)
    currentStream.value = stream
    
    if (videoElement.value) {
      videoElement.value.srcObject = stream
    }
  } catch (error) {
    console.error('Error accessing camera:', error)
    throw error
  }
}

async function switchCamera() {
  stopCamera()
  
  currentCameraIndex.value = (currentCameraIndex.value + 1) % availableCameras.value.length
  
  const newConstraints = {
    video: { 
      deviceId: { exact: availableCameras.value[currentCameraIndex.value].deviceId },
      width: { ideal: props.maxWidth }
    }
  }
  
  try {
    const stream = await navigator.mediaDevices.getUserMedia(newConstraints)
    currentStream.value = stream
    
    if (videoElement.value) {
      videoElement.value.srcObject = stream
    }
  } catch (error) {
    console.error('Error switching camera:', error)
  }
}

function captureImage() {
  const canvas = document.createElement('canvas')
  canvas.width = videoElement.value.videoWidth
  canvas.height = videoElement.value.videoHeight
  canvas.getContext('2d').drawImage(videoElement.value, 0, 0)
  
  imageCapture.value = canvas.toDataURL('image/jpeg')
  emit('image-captured', imageCapture.value)
  
  stopCamera()
}

function retakePhoto() {
  imageCapture.value = null
  initCamera()
}

function confirmImage() {
  if (imageCapture.value) {
    emit('image-confirmed', imageCapture.value)
    
    if (videoElement.value && videoElement.value.srcObject) {
      const tracks = videoElement.value.srcObject.getTracks()
      tracks.forEach(track => track.stop())
    }
  }
}

function cancelCapture() {
  if (videoElement.value && videoElement.value.srcObject) {
    const tracks = videoElement.value.srcObject.getTracks()
    tracks.forEach(track => track.stop())
  }
  
  imageCapture.value = null
  emit('close')
}

function stopCamera() {
  if (currentStream.value) {
    currentStream.value.getTracks().forEach(track => track.stop())
    currentStream.value = null
  }
}
</script>

<style scoped>
.webrtc-camera-container {
  backdrop-filter: blur(10px);
}

.camera-wrapper {
  max-height: 90vh;
  aspect-ratio: 1/1;
}
</style>
