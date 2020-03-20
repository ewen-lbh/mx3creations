<template lang="pug">
  component(v-bind="{...attrs, target}"): slot
</template>

<script>
export default {
  props: {
    url: {
      type: String,
      required: true
    },
    inNewTab: {
      type: Boolean,
      default: null
    },
    fallbackElement: {
      type: String,
      default: 'span'
    }
  },
  computed: {
    isExternal() {
      if (!this.url) return false
      return this.url.startsWith('http')
    },
    target() {
      let inNewTab = false
      if (this.inNewTab !== null) {
        inNewTab = this.inNewTab
      } else {
        inNewTab = this.isExternal
      }
      return inNewTab ? '_blank' : null
    },
    attrs() {
      if (this.url === null) {
        return {
          is: this.fallbackElement
        }
      } else if (this.isExternal) {
        return {
          is: 'a',
          href: this.url
        }
      } else {
        return {
          is: 'nuxt-link',
          to: this.url
        }
      }
    }
  }
}
</script>
