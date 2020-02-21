<template lang="pug">
main
  h1(v-html="collection.name")
  p.description(v-html="collection.description")
  Gallery(:products="collection.products")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'

export default {
  components: { Gallery },
  fetch({ error, route, store, app }) {
    const collections = store.getters['products/collections']
    if (!collections.find((c) => c.id === route.params.collection)) {
      error({ message: 'inexistantCollection', statusCode: 404 })
    }
  },
  computed: {
    ...mapGetters('products', ['products', 'collections']),
    collection() {
      return this.collections.find(
        (c) => c.id === this.$route.params.collection
      )
    }
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-size 10vmin //TODO: Scale down to fit text length, target max fontsize=80px
  font-family Work Sans, sans-serif
  letter-spacing: -0.025em
  // margin-top: -6vmin
  line-height: 0.8
  // color var(--bgi)
</style>
