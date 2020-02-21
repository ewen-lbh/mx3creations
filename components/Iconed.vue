<template lang="pug">
span.--iconed
  img(v-if="icon" :src="`/icons/${icon}.svg`" :class="{ flip }")
  slot
</template>

<script>
export default {
  props: {
    icon: {
      type: String,
      default: null
    },
    flip: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="stylus" scoped>
img
  margin-right: 0.5em
.flip
  transform scaleX(-1)
</style>
