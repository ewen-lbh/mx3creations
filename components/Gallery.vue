<template lang="pug">
.--gallery
  transition-group(tag="div" name="gallery")
    article(
      v-for="work in works"
      :key="work.full_id"
      :class="{ 'has-image': !!getWorkFrontSrc(work), 'has-video': isWorkAVideo(work) }"
    )
      nuxt-link(:to="'/' + work.full_id")
        .video-indicator(v-if="isWorkAVideo(work)" :style="getWorkColors(work, true)")
          Iconed(icon="play" :color="getWorkColors(work, true).color") Vidéo
        .image(v-if="getWorkFrontSrc(work)")
          client-only: progressive-background(
            :src="getWorkFrontSrc(work)"
            :placeholder="getWorkFrontThumbSrc(work)"
            aspect-ratio="1"
            :style="{backgroundColor: work.color || 'black'}"
          )
        .titles(:style="getWorkColors(work)")
          h4(v-if="work.collection") {{ work.collection.name }}
          h3 {{ work.name }}
</template>

<script>
import tinycolor from 'tinycolor2'
import Iconed from '~/components/Iconed.vue'

export default {
  components: { Iconed },
  props: {
    works: {
      type: Array,
      default: null
    }
  },
  methods: {
    getWorkFrontSrc(work) {
      return (
        'https://static.ewen.works/works/' + work.directory + '/thumbs/500.png'
      )
    },
    getWorkFrontThumbSrc(work) {
      return (
        'https://static.ewen.works/works/' + work.directory + '/thumbs/20.png'
      )
    },
    getWorkDetailsHref(work) {
      let path = '/'
      if (work.collection) {
        path += work.collection.id + '/'
      }
      path += work.id
      return path
    },
    getWorkColors(work, reversed = false) {
      const bgColor = work.color || 'black'
      let colors = {
        backgroundColor: bgColor,
        color: tinycolor(bgColor).isLight() ? 'black' : 'white'
      }
      if (reversed) {
        colors = {
          color: colors.backgroundColor,
          backgroundColor: colors.color
        }
      }
      return colors
    },
    isWorkAVideo(work) {
      return (
        (work.youtube.video || work.youtube.playlist) &&
        work.tags.includes('motion design')
      )
    }
  }
}
</script>

<style lang="stylus" scoped>
//
// Variables
//

items-count = auto-fill
min-item-size = 275px
gap = 1em

//
// Layout
//

.--gallery > div
  display grid
  grid-template-columns 'repeat(%s, minmax(%s, 1fr))' % (items-count min-item-size)
  grid-gap gap
  margin 4%

.video-indicator
  position absolute
  top 0.5em
  left 0.5em
  z-index: 100
  padding: 0.5em 1em
  border-radius 0.3333333333em

article
  position relative
  overflow hidden
  animation mouseOut 0.3s ease-in
  min-height min-item-size

.image
  width 100%
  position absolute
  top: 0
  left: 0
  width 100%
  z-index: 0
  object-fit cover
  height 100%

.titles
  padding 2em 1em
  position absolute
  z-index: 10
  top 100%
  left 0
  right: 0
  bottom: 0
  display flex
  justify-self center
  align-items center
  flex-direction column
  transition all 0.25s ease
  h3, h4
    // text-overflow ellipsis
    word-wrap break-word
    word-break break-all
    hyphens auto
  h3
    font-family Work Sans
    font-size 3em
    margin 0
    text-align center
    font-weight normal
    line-height: 0.8

  h4
    text-align center
    font-size 1.5em
    text-transform uppercase
    font-weight bold
    opacity: 0.5
    margin: 0

//
// Reactions
//

article:not(.has-image)
  .titles
    top 0

article.has-image:hover
  .titles
    top 50%
</style>
