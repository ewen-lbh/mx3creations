<template lang="pug">
main
  component.front-cover(
    :src="product.frontCover"
    :is="frontCoverHTMLElement"
    controls
  )
  section
    p.description(v-html="product.description")
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  fetch({ error, route, store, app }) {
    const products = store.getters['products/products']
    if (products.filter((p) => route.params.id === p.id).length === 0) {
      error({ message: 'inexistantWork', statusCode: 404 })
    }
  },
  computed: {
    ...mapGetters('products', ['products', 'all']),
    product() {
      return this.products.find((p) => p.id === this.$route.params.id)
    },
    collection() {
      return this.product.collection
    },
    frontCoverHTMLElement() {
      switch (this.product.type) {
        case 'image':
        case 'pdf':
          return 'img'

        case 'video':
          return 'video'
      }
      return null
    }
  },
  mounted() {
    document.documentElement.style.setProperty('--bg', 'white')
    document.documentElement.style.setProperty('--bgi', 'black')
    document.documentElement.style.setProperty('--fg', 'black')
  }
}
</script>

<style lang="stylus" scoped>
//
// Definitions
//
main
  display flex
  align-items center
  flex-direction column
  width 100%
  background-color var(--bg)
  color var(--bgi)

h1
  font-size 10vmin //TODO: Scale down to fit text length, target max fontsize=80px
  font-family Work Sans, sans-serif
  letter-spacing: -0.025em
  margin-top: -6vmin
  color var(--bgi)

.front-cover
  // width 100%
  // max-width 1000px
  max-height 80vh
  min-height 300px
  object-fit contain
  border 1px solid var(--bgi)
</style>
