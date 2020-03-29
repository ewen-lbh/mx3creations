<template lang="pug">
span.--iconed
  span.icon(v-html="svgContents" :style="`--fill: ${color}`")
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
    },
    color: {
      type: String,
      default: 'var(--text)'
    }
  },
  computed: {
    svgContents() {
      let contents
      try {
        contents = require(`!raw-loader!@/static/icons/${this.icon}.svg`)
          .default
      } catch (error) {
        // eslint-disable-next-line no-console
        console.error(error)
        return ''
      }
      contents = contents.replace(
        '<svg',
        '<svg style="height: 100%; width: 100%; fill: var(--fill) !important;" '
      )
      return contents
    }
  }
}
</script>

<style lang="stylus" scoped>
.icon
  margin-right: 0.5em
  height: 1em

.flip
  transform: scaleX(-1)

.--iconed
  display: flex
  align-items: center
</style>
