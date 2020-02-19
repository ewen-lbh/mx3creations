<template lang="pug">
  h1 {{ collection.name }}
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  fetch({ error, route, store, app }) {
    const products = store.getters['products/all']
    if (products.filter((p) => route.params.collection === p.id).length === 0) {
      error({ message: 'inexistantCollection', statusCode: 404 })
    }
  },
  computed: {
    ...mapGetters('products', ['products', 'all']),
    collection() {
      return this.all.find((p) => p.id === this.$route.params.collection)
    }
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-size 10vmin //TODO: Scale down to fit text length, target max fontsize=80px
  font-family Work Sans, sans-serif
  letter-spacing: -0.025em
  margin-top: -6vmin
  // color var(--bgi)
</style>
