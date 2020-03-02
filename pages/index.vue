<template lang="pug">
main
  h1 {{ $t('myCreations') }}
  section.intro
    p {{ $t('html.intro') }}
    BtnOutline(href="/about") {{ $t('learnMore') }}
  Gallery(v-bind="{products}")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'
import BtnOutline from '~/components/BtnOutline.vue'
export default {
  components: { Gallery, BtnOutline },
  computed: {
    ...mapGetters('products', ['products'])
  }
}
</script>

<style lang="stylus" scoped>
main
  width min(100vw, 1200px)
h1
  font-family Work Sans
  font-size max(10vmin, 3rem)
.intro
  text-align center
  margin-bottom 10vmin
</style>
