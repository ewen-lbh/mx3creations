<template lang="pug">
  BaseBtn.--btn-outline(v-bind="{ ...$attrs, ...$props }" :class="{ small, inverted }"): slot
</template>

<script>
import BaseBtn from '~/components/BaseBtn.vue'

export default {
  components: { BaseBtn },
  props: {
    small: {
      type: Boolean,
      default: false
    },
    inverted: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="stylus" scoped>
.--btn-outline
  --color: var(--text)
  &.inverted
    --color: var(--prim)

.--btn-outline
  background transparent
  border 1px solid var(--color)
  padding 1em
  box-shadow .5em .5em 0 var(--color)
  transition all 0.25s ease
  &.small
    padding: 0.5em
    box-shadow .2em .2em 0 var(--color)
    transition all 0.125s ease

.--btn-outline:hover
  transform translateY(0.4em) translateX(0.4em)
  &.small
    transform translateY(0.1em) translateX(0.1em)
  // &.small
  //   transform translateY(0.1em) translateX(0.1em)
  box-shadow .1em .1em 0 var(--color)
</style>
