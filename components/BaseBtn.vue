<template lang="pug">
  NuxtLinkOrA.--base-btn(
    :url="href"
    fallback-element="button"
    :class="{ clicked, disabled }"
    v-bind="{ disabled }"
    @click="onClicked"
  ): slot
</template>

<script>
import NuxtLinkOrA from '~/components/NuxtLinkOrA.vue'

export default {
  components: { NuxtLinkOrA },
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
