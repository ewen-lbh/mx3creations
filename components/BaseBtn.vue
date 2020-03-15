<template lang="pug">
  component.--base-btn(
    :is="href ? (href.startsWith('http') ? 'a' : 'nuxt-link') : 'button'"
    :to="localePath(href) || false"
    :href="href"
    :target="href.startsWith('http') ? '_blank' : null"
    :class="{ clicked, disabled }"
    v-bind="{ disabled }"
    @click="onClicked"
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
  },
  data() {
    return {
      clicked: false
    }
  },
  methods: {
    onClicked() {
      this.$emit('click')
      this.clicked = true
      setTimeout(() => {
        this.clicked = false
      }, 100)
    }
  }
}
</script>

<style lang="stylus" scoped>
.--base-btn
  display inline-block
  margin 1em
</style>
