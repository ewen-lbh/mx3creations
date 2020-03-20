<template lang="pug">
ul.--technologies-list
  li(v-for="(technology, i) in technologies" :key="i")
    NuxtLinkOrA(:url="getUrl(technology)" :in-new-tab="openInNewTab")
      img.icon(:src="`/logos/${technology}.png`")
      | {{ $t(technology) }}
</template>

<script>
import NuxtLinkOrA from '~/components/NuxtLinkOrA.vue'

export default {
  components: { NuxtLinkOrA },
  props: {
    technologies: {
      type: Array,
      default: () => []
    },
    getUrl: {
      type: Function,
      default: (technology) => null
    },
    openInNewTab: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="stylus" scoped>
li
  display: inline-flex
  align-items: center
  justify-content: center

li:not(:last-child)
  margin-right: 1em

a
  display: flex
  align-items: center
  flex-direction: column
  font-size: 1.2em
  display: flex
  align-items: center
  text-transform: capitalize

.icon
  margin-bottom: 0.5em
  filter: saturate(0)
  height: 3em
  transition: filter 0.25s ease

a:hover .icon
  filter: saturate(1)
</style>
