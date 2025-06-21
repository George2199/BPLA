<!-- src/components/StarField.vue -->
<template>
  <canvas ref="cv" class="star-canvas"></canvas>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

/* ——— настройки ——— */
const MINR = 20;
const MAXR = 50;
const minr1 = MINR * 2.5;
const maxr1 = MAXR * 3.7;
const minr2 = MINR * 1.1;
const maxr2 = MAXR * 0.7;
const minr3 = MINR * 1;
const maxr3 = MAXR * 0.9;

const STAR_CLASSES = [
  { color: '#CDBDF5',  minR:  minr1, maxR: maxr1, amount: [4, 6] }, // мелкие, фиолет
  { color: '#7b5bff',  minR:  minr2, maxR: maxr2, amount: [40, 60]  }, // средние, индиго
  { color: '#fff6b3',  minR:  minr3, maxR: maxr3, amount: [50, 100]  }  // крупные, мягкий жёлтый
]
const MAX_SPEED = 10            // px / кадр
const BOUNCE_LOSS = 0.98         // коэффициент потери скорости при ударе

/* ——— реализация ——— */
const cv = ref(null)
let ctx, stars = [], raf

class Star {
  constructor (cls, w, h) {
    const { minR, maxR, color } = cls
    this.r  = rand(minR, maxR)
    this.x  = rand(this.r, w - this.r)
    this.y  = rand(this.r, h - this.r)
    this.vx = rand(-MAX_SPEED, MAX_SPEED)
    this.vy = rand(-MAX_SPEED, MAX_SPEED)
    this.c  = color
  }
    draw () {
    const r = this.r
    const grad = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, r)
    grad.addColorStop(0, this.c)                       // центр — основной цвет
    grad.addColorStop(0.6, hexToRGBA(this.c, 0.25))    // ближе к краю — чуть прозрачнее
    grad.addColorStop(1,  hexToRGBA(this.c, 0))        // край — полностью прозрачный
    ctx.fillStyle = grad
    ctx.beginPath()

    const spikes = 10
    const t = performance.now() / 300 + this.r + this.x
    const step = (Math.PI * 2) / spikes

    for (let i = 0; i <= spikes; i++) {
        const angle = i * step
        const noise = Math.sin(t + i) * 0.3 + Math.random() * 0.2
        const radius = r * (1 + noise * 0.4)
        const px = this.x + Math.cos(angle) * radius
        const py = this.y + Math.sin(angle) * radius
        if (i === 0) ctx.moveTo(px, py)
        else ctx.lineTo(px, py)
    }

    ctx.closePath()
    ctx.fill()
    }
}

function hexToRGBA(hex, alpha) {
  const rgb = hexToRGB(hex)
  return `rgba(${rgb.r},${rgb.g},${rgb.b},${alpha})`
}

function rand (a, b) { return Math.random() * (b - a) + a }

function spawnStars (w, h) {
  stars = []
  STAR_CLASSES.forEach(cls => {
    const count = Math.floor(rand(...cls.amount))
    for (let i = 0; i < count; i++) stars.push(new Star(cls, w, h))
  })
}

function collide (s1, s2, i, j) {
  const dx = s2.x - s1.x
  const dy = s2.y - s1.y
  const dist = Math.hypot(dx, dy)
  const minDist = s1.r + s2.r
  if (dist < minDist) {
    // — СОЗДАЁМ новую звезду:
    const area = s1.r * s1.r + s2.r * s2.r
    const newR = Math.sqrt(area)
    const newX = (s1.x * s1.r + s2.x * s2.r) / (s1.r + s2.r)
    const newY = (s1.y * s1.r + s2.y * s2.r) / (s1.r + s2.r)
    const newVX = (s1.vx * s1.r + s2.vx * s2.r) / (s1.r + s2.r)
    const newVY = (s1.vy * s1.r + s2.vy * s2.r) / (s1.r + s2.r)
    const newC = mixColors(s1.c, s2.c)

    // Заменим первую звезду новой
    stars[i] = Object.assign(new Star({ minR: newR, maxR: newR, color: newC }, cv.value.width, cv.value.height), {
      x: newX, y: newY, vx: newVX, vy: newVY
    })

    // Удалим вторую звезду
    stars.splice(j, 1)
  }
}

function hexToRGB(hex) {
  const bigint = parseInt(hex.slice(1), 16)
  return {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255,
  }
}

function RGBToHex({ r, g, b }) {
  return `#${[r, g, b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('')}`
}

function mixColors(c1, c2) {
  const rgb1 = hexToRGB(c1)
  const rgb2 = hexToRGB(c2)
  return RGBToHex({
    r: (rgb1.r + rgb2.r) / 2,
    g: (rgb1.g + rgb2.g) / 2,
    b: (rgb1.b + rgb2.b) / 2,
  })
}



function tick () {
  const { width: w, height: h } = cv.value
  ctx.clearRect(0, 0, w, h)

  // движение
  stars.forEach(s => {
    s.x += s.vx
    s.y += s.vy
    // отскок от стен
    if (s.x < s.r || s.x > w - s.r) s.vx *= -BOUNCE_LOSS
    if (s.y < s.r || s.y > h - s.r) s.vy *= -BOUNCE_LOSS
  })

  // столкновения O(n²). норма до ~200 звёзд
    for (let i = 0; i < stars.length; i++) {
    for (let j = i + 1; j < stars.length; j++) {
        if (j >= stars.length) break
        collide(stars[i], stars[j], i, j)
    }
    }


  // рендер
  stars.forEach(s => s.draw())

  raf = requestAnimationFrame(tick)
}

function resize () {
  const dpr = window.devicePixelRatio || 1
  cv.value.width  = innerWidth  * dpr
  cv.value.height = innerHeight * dpr
  ctx.scale(dpr, dpr)     // crisp on HiDPI
  spawnStars(innerWidth, innerHeight)
}

onMounted(() => {
  ctx = cv.value.getContext('2d')
  resize()
  window.addEventListener('resize', resize)
  raf = requestAnimationFrame(tick)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  cancelAnimationFrame(raf)
})
</script>

<style scoped>
.star-canvas{
  position: fixed;
  inset: 0;
  z-index: -2;   /* под всем UI, но поверх фонового цвета */
  pointer-events: none;
}
</style>
