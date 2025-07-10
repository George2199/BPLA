<template>
  <canvas ref="cv" class="royal-canvas"></canvas>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { shared } from '@/components/glowState'

const cv = ref(null)
let ctx, raf

const AMOUNT = 4
const COLORS = ['#c4affa', '#3f14a5', '#7b5bff', '#ff7de9', '#ffc371']
const MIN_RADIUS = 400
const MAX_RADIUS = 1000
const SPEED = 2

class Glow {
  constructor(w, h) {
    this.r = rand(MIN_RADIUS, MAX_RADIUS)
    this.x = rand(0, w)
    this.y = rand(0, h)
    this.vx = rand(-SPEED, SPEED)
    this.vy = rand(-SPEED, SPEED)
    this.c = COLORS[Math.floor(Math.random() * COLORS.length)]
  }

  move(w, h) {
    this.x += this.vx
    this.y += this.vy
    if (this.x < -this.r || this.x > w + this.r) this.vx *= -1
    if (this.y < -this.r || this.y > h + this.r) this.vy *= -1
  }

  draw(ctx) {
    const grad = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.r)
    grad.addColorStop(0, hexToRGBA(this.c, 0.4))
    grad.addColorStop(1, hexToRGBA(this.c, 0))
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
    ctx.fill()
  }
}

function rand(a, b) {
  return Math.random() * (b - a) + a
}

function hexToRGBA(hex, alpha) {
  const rgb = parseInt(hex.slice(1), 16)
  const r = (rgb >> 16) & 255
  const g = (rgb >> 8) & 255
  const b = rgb & 255
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

function tick() {
  if (!ctx || !cv.value) return
  const w = cv.value.width
  const h = cv.value.height

  ctx.clearRect(0, 0, w, h)
  shared.glows.forEach(g => {
    g.move(w, h)
    g.draw(ctx)
  })

  raf = requestAnimationFrame(tick)
  shared.raf = raf
}

function resize() {
  if (!ctx || !cv.value) return
  const dpr = window.devicePixelRatio || 1
  cv.value.width = innerWidth * dpr
  cv.value.height = innerHeight * dpr
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  shared.glows.length = 0
  for (let i = 0; i < AMOUNT; i++) {
    shared.glows.push(new Glow(innerWidth, innerHeight))
  }
}

onMounted(() => {
  ctx = cv.value.getContext('2d')
  shared.ctx = ctx
  shared.canvas = cv.value
  resize()
  window.addEventListener('resize', resize)
  raf = requestAnimationFrame(tick)
  shared.raf = raf
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  cancelAnimationFrame(raf)
})
</script>

<style scoped>
.royal-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
</style>
