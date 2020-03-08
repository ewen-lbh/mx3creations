<template lang="pug">
.--gallery
  PIG(
    :images="pigImages"
    @image-click="handleImageClicked($event)"
  )
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
  mounted() {
    console.log(this.works)
  },
  computed: {
    pigImages() {
      const pigImages = []
      // this.works.forEach((work) => {
      //   product.variants.forEach((variant) => {
      //     if (!variant.size) return
      //     pigImages = [
      //       ...pigImages,
      //       {
      //         filename: variant.src,
      //         aspectRatio: variant.size.aspect_ratio
      //       }
      //     ]
      //   })
      // })
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
    frontCoverHref(product) {
      const cover = product.front_cover
      if (cover.type === 'pdf') {
        return `/works/renders/${product.collection.id}/${product.id}/_thumbnail.png`
      } else {
        return cover.src
      }
    },
    handleImageClicked($event) {
      // http://static.mx3creations.com/works/renders/acf/actualite-des-cartels-2019/0.png
      const idPath = $event
        .replace('http://static.mx3creations.com', '')
        .replace('/works/renders/', '')
        .replace('.png', '')
      console.log(idPath)
      // eslint-disable-next-line no-unused-vars
      const [collectionID, productID, variantID] = idPath.split('/')
      this.$router.push(this.localePath(`/${collectionID}/${productID}`))
    }
  }
}
</script>

<style lang="stylus">
#pig
  width 100%

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
    display none
</style>
