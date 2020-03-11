<template lang="pug">
.--gallery
  ul
    li(v-for="work in works")
      img(:src="getWorkFrontSrc(work)")
      h3
        template(v-if="work.collection")
          | {{ work.collection.name }}
          span.sep /
        | {{ work.name }}
      .description(v-html="work.description")
  //- PIG(
  //-   :images="pigImages"
  //-   @image-click="handleImageClicked($event)"
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
    }
  },
  computed: {
    pigImages() {
      const pigImages = []
      this.works.forEach((work) => {
        pigImages.push({
          filename: '/works/' + work.directory + '/' + work.front,
          aspect_ratio: work.size.aspect_ratio
        })
      })
      console.table(pigImages)
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
      if (work.collection) {
        src += work.collection.id + '/'
      }
      src += work.front
      return src
    }
  }
}
</script>

<style lang="stylus">
h2
  font-family 'Work Sans'
  font-size 6vmin
  text-align center
h3
  font-family 'Work Sans'
  font-size 4vmin

#pig
  width: 100%

.pig-figure
  width: 100%
  height: auto
  margin-bottom: gallery-gaps
  background-color: white !important

  img.pig-loaded:not(.pig-thumbnail)
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
