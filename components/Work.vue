<template lang="pug">
.--work
  h1 {{ name }}
  section.collection(v-if="collection")  
    BtnOutline.collection-link(:href="'/' + collection.id")
      Iconed(icon="arrow-right") En savoir plus sur {{ collection.name }}
  section.links
    ul: li(v-for="(link, i) in links" :key="i")
        BtnOutline(:href="link.url").btn {{ $t(link.name) }}
  section.description(v-html="description")
  section.image
    img(
      v-if="front"
      :src="`/works/${directory}/${front}`"
      importance="high"
    )
    p.no-images(v-else) Pas d'images :/ 
  section.using(v-if="using.length")
    h2 Fait avec...
    ul: li(v-for="(item, i) in using" :key="i")
        a(:href="usingHrefs[item] || item") 
          img.icon(:src="'logos/' + item" onerror="this.style.display='none'")
          | {{ $t(item) }}
          
</template>

<script>
import { mapState } from 'vuex'
import tinycolor from 'tinycolor2'
import Iconed from '~/components/Iconed.vue'
import BtnOutline from '~/components/BtnOutline.vue'

export default {
  components: { Iconed, BtnOutline },
  props: {
    description: {
      type: String,
      default: ''
    },
    name: {
      type: String,
      required: true
    },
    front: {
      type: String,
      default: null
    },
    directory: {
      type: String,
      required: true
    },
    links: {
      type: Object,
      default: () => []
    },
    using: {
      type: Object,
      default: () => []
    },
    collection: {
      type: Object,
      default: null
    },
    color: {
      type: String,
      default: null
    }
  },
  computed: {
    ...mapState('constants', ['usingHrefs'])
  },
  mounted() {
    const backgroundColor = this.color || 'black'
    const color = tinycolor(backgroundColor).isLight() ? 'black' : 'white'
    document.body.style.setProperty('--text', color)
    document.body.style.setProperty('--prim', backgroundColor)
  },
  beforeDestroy() {
    document.body.style.setProperty('--text', null)
    document.body.style.setProperty('--prim', null)
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-size 13vmin
  line-height: 0.8
  font-family Work Sans

img:not(.icon)
  display flex
  justify-content center
  width 100%

.no-images
  background-color rgba(0, 0, 0, 0.0625)
  padding 20em 5em
  text-align center

section.collection
  display flex
  justify-content center
.collection-link
  text-align center
  font-size 1em
  margin 2em auto

.links ul
  display flex
  justify-content center

.using ul
  a
    display flex
    align-items center
    text-transform capitalize
  .icon
    margin-right .5em
</style>
