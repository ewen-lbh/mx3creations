<template lang="pug">
main
  h1 {{ $t('myCreations') }}
  section.intro
    p {{ $t('html.intro') }}
    BtnOutline(href="/about") {{ $t('learnMore') }}
  section(
    v-for="firstTag in workSections"
    :class="firstTag"
  )
    h2 {{ $t(firstTag) }}
    Gallery(:works="ofFirstTag(firstTag)")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'
import BtnOutline from '~/components/BtnOutline.vue'
export default {
  components: { Gallery, BtnOutline },
  data() {
    return {
      workSections: [
        'poster',
        'illustration',
        'drawing',
        'visual-indentity',
        'web',
        'cli'
      ]
    }
  },
  computed: {
    ...mapGetters('works', ['bestOf', 'ofFirstTag'])
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
