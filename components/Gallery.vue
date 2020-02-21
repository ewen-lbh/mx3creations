<template lang="pug">
.gallery
  li(v-for="(product, i) in products" :key="product.gid")
    template(v-if="showProduct(product)")
      nuxt-link(
        :to="localePath(`/${product.collection.id}/${product.id}`)"
        :title="product.title"
      )
        component.item(
          :is="frontCoverHTMLElement(product)"
          :src="frontCoverHref(product)"
          :alt="product.title"
          @load="product.front_cover.type === 'video' ? $el.play() : false"
        ) {{ product.front_cover.src }}
</template>

<script>
export default {
  props: {
    products: {
      type: Array,
      default: null
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
    }
  }
}
</script>

<style lang="stylus" scoped>
//
// Definitions
//

gallery-gaps = 25px

.gallery
  line-height: 0 // Prevent vertical gaps
  column-gap: gallery-gaps

.gallery .item
  width: 100%
  height: auto
  margin-bottom: gallery-gaps
  background white
  border 1px solid black
  transition all 0.25s ease
  box-sizing border-box

.gallery a::before
    content ''
    height: 20px
    background #000
    position absolute

.item:hover
  transform translateY(-10px)
  box-shadow 0 10px 10px rgba(0,0,0,0.4)
  border-color rgba(0,0,0,0.25)
  z-index: -1

.gallery embed.item
  width 100%
  height 100%
  border none

.gallery
  column-count: 5

  @media (max-width: 1200px)
    column-count: 4

  @media (max-width: 1000px)
    column-count: 3

  @media (max-width: 800px)
    column-count: 2

  @media (max-width: 400px)
    column-count: 1
</style>
