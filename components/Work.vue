<template lang="pug">
.--work
  .explain
    section.title
      h1 {{ name }}
      
    section.collection(v-if="collection")
      nuxt-link.name(:to="'/' + collection.id")
        | Collection {{ collection.name }}
      .description(
        v-if="collection.description"
        v-html="collection.description"
      )
      nuxt-link.link(:to="'/' + collection.id")
        Iconed(icon="arrow-right") Voir toutes les créations dans {{ collection.name }}
        
  
    section.date(v-if="year")
      p {{ creationDateString }}

    section.description(v-html="description" v-if="description")
    
  .details
    section.tags(v-if="tags.length")
      h2 Catégories
      ul: li(v-for="(tag, i) in tags" :key="i")
        span.octothorpe #
        nuxt-link(:to="`/tagged/${tag}`") {{ $t(`tags.singular.${tag}`) }}

    section.made-with(v-if="using.length")
      h2 Fait avec...
      TechnologiesList(
        :technologies="using"
        :get-url="(tech) => `/made-with/${tech}`"
      )

  .see
    section.youtube(v-if="youtube.playlist || youtube.video")
      YouTube(v-if="youtube.video" :id="youtube.video")
      YouTube(v-if="youtube.playlist" :id="youtube.playlist" playlist)
    
    section.image
      client-only: progressive-img(
          v-if="front"
          :src="workFrontSrc"
          importance="high"
          :placeholder="workPlaceholderSrc"
          :aspect-ratio="size.aspect_ratio"
        )

    section.links: ul
      li(v-for="(link, i) in links" :key="i")
        BtnOutline(:href="link.url").btn {{ $t(link.name) }}
</template>

<script>
import tinycolor from 'tinycolor2'
import Iconed from '~/components/Iconed.vue'
import BtnOutline from '~/components/BtnOutline.vue'
import TechnologiesList from '~/components/TechnologiesList.vue'
import YouTube from '~/components/YouTube.vue'

export default {
  components: { Iconed, BtnOutline, TechnologiesList, YouTube },
  props: {
    description: {
      type: String,
      default: ''
    },
    wip: {
      type: Boolean,
      default: false
    },
    year: {
      type: Number,
      default: null
    },
    name: {
      type: String,
      required: true
    },
    front: {
      type: String,
      default: null
    },
    size: {
      type: Object,
      default: () => ({
        height: null,
        width: null,
        aspect_ratio: null
      })
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
    tags: {
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
    },
    youtube: {
      type: Object,
      default: () => ({
        playlist: null,
        video: null
      })
    }
  },
  computed: {
    workFrontSrc() {
      let src = ''
      src = 'https://static.ewen.works'
      if (process.env.NODE_ENV === 'production') {
      }
      src += '/works/'
      if (this.front === null) return null
      src += this.directory + '/' + this.front
      return src
    },
    workPlaceholderSrc() {
      let src = ''
      src = 'https://static.ewen.works'
      if (process.env.NODE_ENV === 'production') {
      }
      src += '/works/'
      if (this.front === null) return null
      src += this.directory + `/thumbs/20.png`
      return src
    },
    yearDiff() {
      if (!this.year) return null
      return new Date().getFullYear() - this.year
    },

    creationDateString() {
      if (this.wip) return `Commencé en ${this.year} (en cours)`
      if (this.yearDiff === 0) return `Créé cette anée`
      if (this.yearDiff === 1) return `Créé l'année dernière`
      if (this.yearDiff > 1) return `Créé il y a ${this.yearDiff} ans`
      return ''
    }
  },
  mounted() {
    const backgroundColor = this.color || 'white'
    const color = tinycolor(backgroundColor).isLight() ? 'black' : 'white'
    document.body.style.setProperty('--text', color)
    document.body.style.setProperty('--prim', backgroundColor)
    window.scrollTo(0, 0)
  },
  beforeDestroy() {
    document.body.style.setProperty('--text', null)
    document.body.style.setProperty('--prim', null)
  }
}
</script>

<style lang="stylus" scoped>
//
// Variables
//

area(area)
  .{area}
    grid-area area

//
// Layout
//

.--work
  // Layout
  area(explain); area(details); area(see)
  display grid
  grid-template-areas: 'explain see' 'details see'
  grid-template-columns 1.5fr 1fr

  // Width
  width 100%

  // Spacing
  grid-gap 2em

section
  margin-left 0

h1
  text-align left

section.collection
  &
    margin-bottom 3em
  .description, .link
    padding-left 3em
  .link
    display inline-block // Prevents overflow on mobile

section.description
  margin-bottom 3em
  max-width 600px

section.youtube
  margin-bottom 2em

section.links
  text-align center

section.tags
li
  display inline-block

//
// Typography
//

h1
  font-size unquote("max(10vmin, 4em)")
  line-height: 0.7
  font-family Work Sans
  margin-bottom: 0.125em
.collection .name
  font-size unquote("max(5vmin, 1.5em)")

section.date
  font-size 1.2em
  font-weight bold
  opacity 0.5
  // mix-blend-mode overlay

section.collection
  .name
    text-transform uppercase
  .name, .link
    font-weight bold
    opacity: 0.5
    // mix-blend-mode overlay

section.tags
  li
    font-size 1.2em
    line-height: 1.5
  li:not(:last-child)
    margin-right 1em
  .octothorpe
    opacity: 0.25
  a
    transition opacity 0.25 ease
  a:hover
    opacity: 0.25

//
// Misc
//

section.image /deep/
  & .progressive-image
    overflow visible // Fix, if set to hidden the bottom border is not visible.
  & img
    border 1px solid var(--text)
    box-sizing border-box

//
// Reactions
//

section.collection
  a:hover
    opacity: 1

//
// Responsive layout
//

@media (max-width: 820px)
  .--work
    grid-template-areas 'explain' 'see' 'details'
    grid-template-columns 1fr
</style>
