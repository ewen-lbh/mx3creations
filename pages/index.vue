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
    h2 {{ $t('tags.plural.'+firstTag) }}
    
    Gallery(:works="bestOf(ofFirstTag(firstTag))" :id="firstTag")
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
        'visual identity',
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
  width min(100vw, 1400px)

h1
  font-family Work Sans
  font-size max(10vmin, 3rem)
.intro
  text-align center
  margin-bottom 10vmin

section:not(.intro)
  max-width unset

h2
  height: 70px //ref:<TheNavbar>/height
  font-family: 'Inconsolata'
  font-size: 1.5em
  text-transform uppercase
  display flex
  align-items center
  justify-content center
  position sticky
  top: 0
  // mix-blend-mode difference
  // color white
  z-index: 1000

.--gallery
  width 100%
</style>
