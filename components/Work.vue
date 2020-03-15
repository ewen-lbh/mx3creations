<template lang="pug">
.--work
  h1 {{ name }}
  section.collection(v-if="collection")  
    nuxt-link.collection-link(:to="'/' + collection.id")
      Iconed(icon="arrow-right") En savoir plus sur {{ collection.name }}
  section.links
    ul: li(v-for="(link, i) in links" :key="i")
        BtnOutline(:href="link.url").btn {{ $t(link.name) }}
  section.description(v-html="description")
  section.image
    img(
      v-if="front"
      :src="workFrontSrc"
      importance="high"
    )
    p.no-images(v-else) Pas d'images :/ 
  section.using(v-if="using.length")
    h2 Fait avec...
    ul: li(v-for="(item, i) in using" :key="i")
        component(
          :is="usingHrefs[item] ? 'a' : 'span'"
          :href="usingHrefs[item]"
          target="_blank"
        )
          img.icon(:src="`/logos/${item}.png`")
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
    ...mapState('constants', ['usingHrefs']),
    workFrontSrc() {
      let src = ''
      if (process.env.NODE_ENV === 'production') {
        src = 'https://static.mx3creations.com'
      }
      src += '/works/'
      if (this.front === null) return null
      src += this.directory + '/' + this.front
      return src
    }
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
  font-size: 13vmin
  line-height: 0.8
  font-family: Work Sans

img:not(.icon)
  display: flex
  justify-content: center
  width: 100%
  object-fit contain
  max-height 75vh

.no-images
  background-color: rgba(0, 0, 0, 0.0625)
  padding: 20em 5em
  text-align: center

section.collection
  display: flex
  justify-content: center

.collection-link
  text-align: center
  font-size: 1.2em
  margin-top: 2em
  font-style: italic
  font-weight: bold
  opacity: 0.5
  transition: opacity 0.25s ease

  &:hover
    opacity: 1

.links ul
  display: flex
  justify-content: center
  margin-bottom: 2em
  margin-top: 0

  .btn
    text-transform: capitalize

section.using
  h2
    text-align: center
    font-weight: normal
    font-size: 2.5em

  ul
    display: inline-block
    margin: 0 auto

  li
    display: inline-flex
    align-items: center
    justify-content: center

  li:not(:last-child)
    margin-right: 1em

  a
    display: flex
    align-items: center
    flex-direction: column
    font-size: 1.2em
    display: flex
    align-items: center
    text-transform: capitalize

  .icon
    margin-bottom: 0.5em
    filter: saturate(0)
    height: 3em
    transition: filter 0.25s ease

  a:hover .icon
    filter: saturate(1)
</style>
