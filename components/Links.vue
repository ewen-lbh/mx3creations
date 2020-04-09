<template lang="pug">
ul.--links: li(v-for="(link, i) in links" :key="i")
  BtnOutline(:href="link.url").btn {{ $t(link.name) }}
</template>

<script>
import BtnOutline from '~/components/BtnOutline.vue'

export default {
  components: { BtnOutline },
  props: {
    links: {
      type: Object,
      default: () => []
    }
  }
}
</script>

<style lang="stylus" scoped>
ul
  display flex
</style>
