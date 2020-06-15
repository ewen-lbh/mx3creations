<template lang="pug">
main
  h1 {{ $t('myCreations') }}
  section.intro
    p {{ $t('indexPage.intro') }}
    BtnOutline(href="/about") {{ $t('learnMore') }}
  section(
    v-for="firstTag in workSections"
    :class="firstTag"
  )
    h2
      | {{ $t('tags.plural.'+firstTag) }}
      nuxt-link(:to="`/tagged/${firstTag}`")
        Iconed(icon="arrow-right") {{ $t('See all') }}

    Gallery(:works="bestOf(ofFirstTag(firstTag))" :id="firstTag")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'
import BtnOutline from '~/components/BtnOutline.vue'
import Iconed from '~/components/Iconed.vue'
export default {
  components: { Gallery, BtnOutline, Iconed },
  data() {
    return {
      workSections: [
        'poster',
        'illustration',
        'music',
        'visual identity',
        'web',
        'program',
        'typography',
        'motion design'
      ]
    }
  },
  computed: {
    ...mapGetters('works', ['bestOf', 'ofFirstTag', 'ofTag'])
  },
  methods: {
    hasMoreWorksThanShown(tag) {
      return this.bestOf(this.ofFirstTag(tag)).length < this.withTags([tag])
    }
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
  font-family: 'Inconsolata'
  font-size: 1.5em
  text-transform uppercase
  text-align center
  display flex
  align-items center
  a
    margin-left auto

.--gallery
  width 100%
</style>
