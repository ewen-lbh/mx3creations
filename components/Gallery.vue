<template lang="pug">
.--gallery
  ul
    template(v-for="(work, i) in works")
      li(v-if="getWorkFrontSrc(work)" :key="i")
        nuxt-link(:to="getWorkDetailsHref(work)")
          img(
            :src="getWorkFrontSrc(work)"
            :title="work.name"
          )
          h3
            template(v-if="work.collection")
              | {{ work.collection.name }}
              span.sep /
            | {{ work.name }}

  //- PIG(
  //-   :images="pigImages"
  //-   @image-click="handleImageClicked($event)",
  //-   :pig-id="'pig-' + id"
  //-   style="height:100vh;"
  //- )
</template>

<script>
import PIG from '~/components/PIG.vue'

export default {
  components: { PIG },
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
      return 'https://placehold.it/500/500'
      // eslint-disable-next-line no-unreachable
      let src = '/works/'
      if (work.front === null) return null
      src += work.directory + '/' + work.front
      return src
    },
    getWorkDetailsHref(work) {
      let path = '/'
      if (work.collection) {
        path += work.collection.id
      }
      path += work.id
      return path
    }
  }
}
</script>

<style lang="stylus" scoped>
h3
  font-family: 'Work Sans'
  font-size: 2em
  text-align center
  font-weight normal
  margin-top: 0

ul
  height: 300px
  display flex
  align-items center
li
  height 100%
img
  object-fit contain
  height: 100%

.description
  a
    border 1px solid transparent
    border-bottom 1px solid black
  a:hover
    border 1px solid black

.--pig
  width: 100%

.--pig .pig-figure
  width: 100% !important
  height: auto !important
  margin-bottom: gallery-gaps
  background-color: white !important

  img.pig-loaded:not(.pig-thumbnail)
    height auto
    transition: all 0.25s ease !important
    box-sizing: border-box
    // border: 1px solid black

.pig-figure:hover
  overflow: visible !important

  img.pig-loaded:not(.pig-thumbnail)
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25)
    transform: translateY(-10px)
    position: absolute

  img.pig-thumbnail
    display: none
</style>
