<template lang="pug">
span.--iconed
  svg(viewBox="0 0 35 18"): use(:href="`/icons/${icon}.svg#path`" style="--fill: var(--text)")
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
svg
  margin-right: 0.5em
  height 1em
.flip
  transform scaleX(-1)
.--iconed
  display flex
  align-items center
</style>
