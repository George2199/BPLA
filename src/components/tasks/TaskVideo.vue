<template>
  <div class="responsive-video">
    <video
      ref="videoPlayer"
      width="100%"
      controls
      @play="onPlay"
      @pause="onPause"
      @ended="onVideoEnd"
      @timeupdate="updateProgress"
    >
      <source :src="computedVideoUrl" type="video/mp4" />
    </video>
    <div class="controls">
      <button @click="togglePlay">{{ isPlaying ? 'Пауза' : 'Играть' }}</button>
      <input 
        type="range" 
        v-model="progress"
        @input="seek"
        max="100"
      >
      <span>{{ formattedTime }} / {{ formattedDuration }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { API_BASE_URL } from '@/api'
const props = defineProps({
  task: Object
})

// Поддержка ссылок вида "/data/videos/lesson1.mp4"
const computedVideoUrl = computed(() => {
  return props.task?.video_path ? `${API_BASE_URL}/${props.task.video_path}` : ''
})

const videoPlayer = ref(null)
const isPlaying = ref(false)
const progress = ref(0)
const currentTime = ref(0)
const duration = ref(0)

const togglePlay = () => {
  if (!videoPlayer.value) return;
  if (videoPlayer.value.paused) {
    videoPlayer.value.play()
  } else {
    videoPlayer.value.pause()
  }
}

const onPlay = () => isPlaying.value = true
const onPause = () => isPlaying.value = false
const onVideoEnd = () => {
  isPlaying.value = false;
  progress.value = 0;
  currentTime.value = 0;
}

const updateProgress = () => {
  if (!videoPlayer.value) return;
  const video = videoPlayer.value;
  progress.value = (video.currentTime / video.duration) * 100;
  currentTime.value = video.currentTime;
  if (!duration.value && video.duration) {
    duration.value = video.duration;
  }
}

const seek = (e) => {
  if (!videoPlayer.value || !videoPlayer.value.duration) return;
  const seekTo = videoPlayer.value.duration * (e.target.value / 100)
  videoPlayer.value.currentTime = seekTo
}

const formatTime = (timeInSeconds) => {
  if (isNaN(timeInSeconds) || timeInSeconds === Infinity) {
    return '00:00';
  }
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = Math.floor(timeInSeconds % 60);
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

const formattedTime = computed(() => formatTime(currentTime.value))
const formattedDuration = computed(() => formatTime(duration.value))
</script>


<style scoped>
.responsive-video {
  position: relative;
  width: 100%;
  height: auto;
  max-width: 100%;
  background: #000;
  display: flex;
  flex-direction: column;
  border-radius: inherit; /* ← добавь вот это */
}


.responsive-video video {
  width: 100%;
  height: auto;
  border-radius: inherit; /* ← добавь вот это */
}


.controls {
  position: absolute;
  bottom: 10px;
  left: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.5);
  padding: 5px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.responsive-video:hover .controls {
  opacity: 1;
}

.controls input[type="range"] {
  flex-grow: 1;
}

.controls button {
  background: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}

.responsive-video:hover video::-webkit-media-controls {
    display: none !important;
}
.responsive-video:hover video::-moz-media-controls {
    display: none !important;
}
.responsive-video:hover video::-ms-media-controls {
    display: none !important;
}
.responsive-video:hover video::media-controls {
    display: none !important;
}
</style>