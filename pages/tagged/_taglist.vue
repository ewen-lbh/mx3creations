<template lang="pug">
main
  h1 {{ taglistDisplay }}
  Gallery(:works="worksOfTags")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'

export default {
  components: { Gallery },
  computed: {
    ...mapGetters('works', ['all']),
    worksOfTags() {
      let filtered = []
      this.$route.params.taglist.split(',').forEach((t) => {
        filtered = [...filtered, ...this.all.filter((p) => p.tags.includes(t))]
      })
      return filtered
    },
    taglistDisplay() {
      const tags = this.$route.params.taglist
        .split(',')
        .map((tag) => this.$t('tags.plural.' + tag))
        .map((tag) => tag.replace('tags.plural.', ''))
        .join(', ')
        .replace(/, ([^,]*)$/, ` ${this.$t('and')} $1`)
        .replace(/^(.)/, ($0, $1) => $1.toUpperCase())
      return tags
    }
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-size max(10vmin, 3rem)
  text-align center
  margin 0
</style>
