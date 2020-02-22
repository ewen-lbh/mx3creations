<template lang="pug">
.--gallery
  PIG(
    :images="pigImages"
    @image-click="handleImageClicked($event)"
  )
  //- li(v-for="(product, i) in products" :key="product.gid")
  //-   template(v-if="showProduct(product)")
  //-     nuxt-link(
  //-       :to="localePath(`/${product.collection.id}/${product.id}`)"
  //-       :title="product.title"
  //-     )
  //-       component.item(
  //-         :is="frontCoverHTMLElement(product)"
  //-         :src="frontCoverHref(product)"
  //-         :alt="product.title"
  //-         :style="{ height: product.front_cover.size ? product.front_cover.size.height + 'px' : 'auto' }"
  //-       ) {{ product.front_cover.content }}
</template>

<script>
import PIG from '~/components/PIG.vue'

export default {
  components: { PIG },
  props: {
    products: {
      type: Array,
      default: null
    }
  },
  computed: {
    pigImages() {
      let pigImages = []
      this.products.forEach((product) => {
        product.variants.forEach((variant) => {
          if (!variant.size) return
          pigImages = [
            ...pigImages,
            { filename: variant.src, aspectRatio: variant.size.aspect_ratio }
          ]
        })
      })
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
        return `/products/renders/${product.collection.id}/${product.id}/_thumbnail.png`
      } else {
        return cover.src
      }
    },
    handleImageClicked($event) {
      // http://static.mx3creations.com/products/renders/acf/actualite-des-cartels-2019/0.png
      const idPath = $event
        .replace('http://static.mx3creations.com/products/renders/', '')
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
.pig-figure
  width: 100%
  height: auto
  margin-bottom: gallery-gaps
  background white
  box-sizing border-box
  overflow visible !important
  background-color white !important
  img.pig-loaded
    transition all 0.25s ease !important
    border 1px solid black
  img.pig-thumbnail
    filter none !important
    display none

.pig-figure:hover
  img.pig-loaded:not(.pig-thumbnail)
    box-shadow 0 10px 30px rgba(0,0,0,0.4)
    transform translateY(-10px)
    position absolute
</style>
