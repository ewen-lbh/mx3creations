<template lang="pug">
  component.--base-btn(
    :is="href ? 'nuxt-link' : 'button'"
    :to="localePath(href) || false"
    :class="{ clicked, disabled }"
    v-bind="{ disabled }"
  ): slot
</template>

<script>
export default {
  props: {
    href: {
      type: String,
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="stylus" scoped>
.--base-btn
  display inline-block
</style>
