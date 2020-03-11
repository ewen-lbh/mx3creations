<template lang="pug">
.--gallery
  ul
    template(v-for="(work, i) in works")
      li(v-if="getWorkFrontSrc(work)" :key="i")
        //- h3
        //-   template(v-if="work.collection")
        //-     | {{ work.collection.name }}
        //-     span.sep /
        //-   | {{ work.name }}
        img(
          :src="getWorkFrontSrc(work)"
        )

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
  computed: {
    pigImages() {
      let pigImages = []
      this.works.forEach((work) => {
        pigImages.push({
          filename: this.getWorkFrontSrc(work),
          aspect_ratio: work.size.aspect_ratio
        })
      })
      pigImages = pigImages.filter((img) => img.filename)
      console.dir(pigImages)
      return pigImages
    }
  },
  methods: {
    frontCoverHTMLElement(product) {
      switch (product.front_cover.type) {
        case 'image':
        case 'pdf':
          return 'img'

        case 'video':
          return 'video'
      }
      return null
    },
    showProduct(product) {
      return (
        product &&
        product.front_cover !== undefined &&
        !product.hide_from.includes('gallery') &&
        this.frontCoverHTMLElement(product)
      )
    },
    handleImageClicked($event) {
      // http://static.mx3creations.com/works/renders/acf/actualite-des-cartels-2019/0.png
      const idPath = $event
        .replace('http://static.mx3creations.com', '')
        .replace('/works/', '')
        .replace('.png', '')
      console.log(idPath)
      // eslint-disable-next-line no-unused-vars
      const [collectionID, productID, variantID] = idPath.split('/')
      this.$router.push(this.localePath(`/${collectionID}/${productID}`))
    },
    getWorkFrontSrc(work) {
      let src = '/works/'
      if (work.front === null) return null
      src += work.directory + '/' + work.front
      return src
    }
  }
}
</script>

<style lang="stylus" scoped>
h3
  font-family: 'Work Sans'
  font-size: 4vmin

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
