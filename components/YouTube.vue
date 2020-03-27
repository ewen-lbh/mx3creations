<template lang="pug">
.video-wrapper.--youtube: iframe(
  :src='src'
  frameborder='0'
  allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'
  allowfullscreen playsinline
  width="100%"
  height="100%"
)
</template>

<script>
export default {
  props: {
    id: {
      type: String,
      required: true
    },
    playlist: {
      type: Boolean,
      default: false
    },
    allowCookies: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    src() {
      const protocol = 'https://'
      const domain = this.allowCookies
        ? 'www.youtube.com'
        : 'www.youtube-nocookie.com'
      const path = this.playlist
        ? `/embed/videoseries?list=${this.id}`
        : `/embed/${this.id}`
      return protocol + domain + path
    }
  }
}
</script>

<style lang="stylus" scoped>
.video-wrapper
  position relative
  padding-bottom: 56.25%
  width: 100%
iframe
  position absolute
</style>
