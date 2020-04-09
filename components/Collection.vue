<template lang="pug">
main
  h1 {{ name }}
  section.links: Links(:links="links")
  section.description(v-html="description")
  h2 Projets dans cette collection
  Gallery(:works="ofCollection(id)")
</template>

<script>
import { mapGetters } from 'vuex'
import Links from '~/components/Links.vue'
import Gallery from '~/components/Gallery.vue'

export default {
  components: { Gallery, Links },
  props: {
    name: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: null
    },
    id: {
      type: String,
      required: true
    },
    links: {
      type: Object,
      default: () => []
    }
  },
  computed: {
    ...mapGetters('works', ['ofCollection'])
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-size 13vmin
  line-height: 0.8
  font-family Work Sans

h2
  font-size 3em
  line-height: 0.8
  font-family Work Sans
  text-align center

.--links
  justify-content center
</style>
