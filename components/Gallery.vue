<template lang="pug">
.--gallery
  transition-group(tag="div" name="gallery")
    article(
      v-for="work in works"
      :key="work.full_id"
      :class="{ 'has-image': !!getWorkFrontSrc(work) }"
    )
      nuxt-link(:to="'/' + work.full_id")
        .image(v-if="getWorkFrontSrc(work)")
          img(:src="getWorkFrontSrc(work)")
        .titles(:style="getWorkColors(work)")
          h4(v-if="work.collection") {{ work.collection.name }}
          h3 {{ work.name }}
</template>

<script>
import tinycolor from 'tinycolor2'

export default {
  props: {
    works: {
      type: Array,
      default: null
    }
  },
  methods: {
    getWorkFrontSrc(work) {
      // eslint-disable-next-line no-unreachable
      let src = '/works/'
      if (work.front === null) return null
      src += work.directory + '/' + work.front
      return src
    },
    getWorkFrontSrcSet(work) {
      const thumbsDir = work.directory + '/thumbs/'
      const srcset = {
        '1x': this.getWorkFrontSrc(work),
        '20w': thumbsDir + '20.png',
        '150w': thumbsDir + '150.png',
        '500w': thumbsDir + '500.png'
      }
      let srcsetString = ''
      Object.entries(srcset).forEach(([sizeDescriptor, src]) => {
        srcsetString += src + ' ' + sizeDescriptor + ', '
      })
      srcsetString.replace(/,$/, '')
      return srcsetString
    },
    getWorkDetailsHref(work) {
      let path = '/'
      if (work.collection) {
        path += work.collection.id + '/'
      }
      path += work.id
      return path
    },
    getWorkColors(work) {
      const bgColor = work.color || 'black'
      return {
        backgroundColor: bgColor,
        color: tinycolor(bgColor).isLight() ? 'black' : 'white'
      }
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
gap = 2px

//
// Layout
//

.--gallery > div
  display grid
  grid-template-columns 'repeat(%s, minmax(%s, 1fr))' % (items-count min-item-size)
  grid-gap gap
  margin 4%

article
  position relative
  overflow hidden
  animation mouseOut 0.3s ease-in

.image
  position relative
  width 100%
.image::after
  // Forces the container to be a square
  content ''
  display block
  padding-bottom 100%
img
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
