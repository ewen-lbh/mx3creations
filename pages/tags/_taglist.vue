<template lang="pug">
  h1 {{ taglistDisplay }}
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'

export default {
  components: { Gallery },
  computed: {
    ...mapGetters('products', ['products']),
    productsOfTags() {
      let filtered = []
      this.$route.params.taglist.split('+').forEach((t) => {
        filtered = [
          ...filtered,
          ...this.products.filter((p) => p.tags.includes(t))
        ]
      })
      return filtered
    },
    taglistDisplay() {
      const tags = this.$route.params.taglist
        .split('+')
        .map((tag) => this.$t('tags.' + tag))
        .map((tag) => tag.replace('tags.', ''))
        .map((tag) =>
          tag
            .split(' ')
            .map((w) => w + 's')
            .join(' ')
        )
        .join(', ')
        .replace(/, ([^,]*)$/, ` ${this.$t('and')} $1`)
        .replace(/^(.)/, ($0, $1) => $1.toUpperCase())
      return tags
    }
  }
}
</script>
