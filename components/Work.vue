<template lang="pug">
.--work
  section(fullwidth).title
    h1 
  h1 
    h1 
      span.work-name {{ name }}
      nuxt-link.collection-name(
        v-if="collection"
        :to="'/' + collection.id"
      ) Collection {{ collection.name }}
  section.links
    ul: li(v-for="(link, i) in links" :key="i")
        BtnOutline(:href="link.url").btn {{ $t(link.name) }}
  section.collection-description(v-if="collection && collection.description")
    h2 À propos de la collection
    .description(v-html="collection.description")
  section.collection(v-if="collection")  
    nuxt-link.collection-link(:to="'/' + collection.id")
      Iconed(icon="arrow-right") Œuvres de la collection
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
    TechnologiesList(
      :technologies="using"
      :get-url="(tech) => `/made-with/${tech}`"
    )
</template>

<script>
import tinycolor from 'tinycolor2'
import Iconed from '~/components/Iconed.vue'
import BtnOutline from '~/components/BtnOutline.vue'
import TechnologiesList from '~/components/TechnologiesList.vue'

export default {
  components: { Iconed, BtnOutline, TechnologiesList },
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
    const backgroundColor = this.color || 'white'
    const color = tinycolor(backgroundColor).isLight() ? 'black' : 'white'
    document.body.style.setProperty('--text', color)
    document.body.style.setProperty('--prim', backgroundColor)
  },
  beforeDestroy() {
    // document.body.style.setProperty('--text', null)
    // document.body.style.setProperty('--prim', null)
  }
}
</script>

<style lang="stylus" scoped>
h1
  display flex
  flex-direction column
  align-items center
h1 .work-name
  font-size: 13vmin
  line-height: 0.8
  font-family: Work Sans
h1 .collection-name
  font-size: 3vmin
  opacity: 0.5
  text-transform uppercase
  transition opacity 0.25s ease
  &:hover
    opacity: 0.25

img:not(.icon)
  display: flex
  justify-content: center
  width: 100%
  object-fit contain
  max-height 75vh
  border 1px solid var(--text)

.no-images
  background-color: rgba(0, 0, 0, 0.0625)
  padding: 20em 5em
  text-align: center

section.collection-description h2
  font-family Work Sans
  font-size: 5vmin
  margin-bottom -.25em

section.collection
  display: flex
  justify-content: center

.collection-link
  text-align: center
  font-size: 1.2em
  margin-top 1em
  margin-bottom: 2em
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

section.using
  h2
    text-align: center
    font-weight: normal
    font-size: 2.5em

  .--technologies-list
    display flex
    justify-content center
</style>
