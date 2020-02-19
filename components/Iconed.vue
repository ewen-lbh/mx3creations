<template lang="pug">
span.--iconed
  img(v-if="icon" :src="`/icons/${icon}.svg`")
  slot
</template>

<script>
export default {
  props: {
    icon: {
      type: String,
      default: null
    }
  }
}
</script>

<style lang="stylus" scoped>
img
  margin-right: 0.5em
</style>
