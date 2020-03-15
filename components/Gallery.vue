<template lang="pug">
.--gallery
  ul
    template(v-for="(work, i) in works")
      li(:key="i")
        nuxt-link(:to="getWorkDetailsHref(work)")
          .titles-layer(:style="getWorkTitlesLayerStyles(work)")
            h4.collection(v-if="work.collection") {{ work.collection.name }}
            h3.name {{ work.name }}
            p.description(v-html="work.description || work.collection.description")
          img(
            :src="getWorkFrontSrc(work)"
            :srcset="getWorkFrontSrcSet(work)"
            :title="work.name"
          )
</template>

<script>
import tinycolor from 'tinycolor2'

export default {
  props: {
    works: {
      type: Array,
      default: null
    },
    id: {
      type: String,
      required: true
    }
  },
  mounted() {
    console.dir(this.works)
    console.table(
      this.works.map((w) => ({ id: w.id, src: this.getWorkFrontSrc(w) }))
    )
  },
  methods: {
    getWorkFrontSrc(work) {
      // eslint-disable-next-line no-unreachable
      let src = '/works/'
      if (work.front === null) return 'https://placehold.it/500/500'
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
    getWorkTitlesLayerStyles(work) {
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
ul
  height: 600px
  display flex
  align-items center
li
  height 100%
  position relative
  padding: 0
  margin: 0

img
  object-fit contain
  height: 100%

li:hover
  .titles-layer
    opacity: 0.80
    backdrop-filter blur(10px)
    transform scale(1)

.titles-layer
  position absolute
  background-color black
  overflow hidden
  display flex
  flex-direction column
  justify-content center
  align-items center
  opacity: 0
  transform scale(0)
  height 100%
  width 100%
  transition all 0.25s cubic-bezier(.7,.34,.25,1)
  h3, h4, p
    padding 0 2em
    margin 0
    opacity: 1
    text-align center
  p
    text-align left
    max-height 50%
    overflow hidden
    text-overflow ellipsis
  .name
    font-size 5em
    font-family Work Sans
    line-height: 0.8
  .collection
    font-size: 2em
    text-transform uppercase
    opacity: 0.75
    font-weight normal

.description
  a
    border 1px solid transparent
    border-bottom 1px solid black
  a:hover
    border 1px solid black
</style>
