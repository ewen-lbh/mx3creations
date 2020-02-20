<template lang="pug">
#page
  h1 {{ $t('hello') }}
  section.intro
    p {{ $t('intro') }}
    BtnOutline(href="/about") {{ $t('learnMore') }}
  Gallery
</template>

<script>
import Gallery from '~/components/Gallery.vue'
import BtnOutline from '~/components/BtnOutline.vue'
export default {
  components: { Gallery, BtnOutline }
}
</script>

<style lang="stylus" scoped>
h1
  font-family Work Sans
  font-size max(10vmin, 3rem)
.intro
  text-align center
  margin-bottom 10vmin
</style>
