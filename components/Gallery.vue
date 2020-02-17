<template lang="pug">
section.gallery
  li(v-for="(product, i) in productsOfCategory" :key="`${product.collection.id}/${product.id}`")
    template(v-if="showProduct(product)")
      nuxt-link(
        :to="`/works/${product.collection.id}/${product.id}`"
        :title="product.frontCover"
      )
        component.item(
          :is="frontCoverHTMLElement(product.type)"
          :src="'https://mx3creations.com/.netlify/large-media' + product.frontCover"
          :alt="product.title"
          autoplay muted loop
        )
</template>

<script>
import { mapGetters } from 'vuex'
import { firstBy } from 'thenby'

export default {
  props: {
    category: {
      type: String,
      default: null
    }
  },
  computed: {
    ...mapGetters('products', ['products']),
    productsOfCategory() {
      if (!this.category) return this.products
      return this.products
        .filter((product) => product.categories.includes(this.category))
        .sort(firstBy('collection.date').thenBy('id'))
    }
  },
  methods: {
    frontCoverHTMLElement(productType) {
      switch (productType) {
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
        product.frontCover &&
        !product.hideFrom.includes('gallery') &&
        this.frontCoverHTMLElement(product.type)
      )
    }
  }
}
</script>

<style lang="stylus" scoped>
gallery-gaps = 0.25em

.gallery
  line-height: 0 // Prevent vertical gaps
  column-gap: gallery-gaps

.gallery .item
  width: 100%
  height: auto
  margin-bottom: gallery-gaps
  background white
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
