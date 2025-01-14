<template>
  <div>
    <canvas ref="canvas" style="position: absolute; z-index: 0; top: 0; left: 0;width: 100%; height: 100%;"></canvas>
  </div>
</template>
 
<script>
import confetti from 'canvas-confetti'
export default {
  data() {
    return {
      animationId: null,
      isPaused: false,
      myConfetti: null,
    }
  },
  mounted() {
    // 初始化 confetti 附加在指定的 canvas 元素上
    this.myConfetti = confetti.create(this.$refs.canvas, {
      resize: true // 画布会自动全屏
    });
    this.animateConfetti()
  },
  beforeDestroy() {
    this.cleanup()
  },
  methods: {
    // 离开页面时，清除定时器
    cleanup() {
      if (this.animationId) {
        cancelAnimationFrame(this.animationId);
        this.animationId = null;
      }
      if (this.myConfetti) {
        confetti.reset();
        this.myConfetti.reset(); // 如果 confetti 库提供 reset 方法
        this.myConfetti = null;
      }
    },
    animateConfetti() {
      if (this.isPaused) {
        return;
      }
      let end = Date.now() + (15 * 1000);
      let colors = ['#bb0000', '#f8d17c'];
      const playConfetti = (angle, originX) => {
        this.myConfetti({
          particleCount: 2,
          angle,
          spread: 55,
          origin: { x: originX },
          colors: colors,
          done: () => {
            console.log(`Confetti from angle ${angle} finished`);
          }
        });
      };
 
      playConfetti(60, 0);
      playConfetti(120, 1);
 
      if (Date.now() < end) {
        // 下一帧
        this.animationId = requestAnimationFrame(this.animateConfetti);
      } else {
        this.isPaused = true
      }
    }
  }
};
</script>
<style lang="scss" scoped>
</style>