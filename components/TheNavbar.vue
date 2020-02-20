<template lang="pug">
.nav-wrapper(:class="{ scrolled }")
  nav
    template(v-if="backURL")
      NavItem.go-back(:to="backURL"): Iconed(icon="arrow-left") {{ $t('back') }}
    template(v-else)
      NavItem(to="/") {{ $t('works') }}
      NavItem(to="/about") {{ $t('about') }}
      NavItem(to="/contact") {{ $t('contact') }}

    span.center.breadcrumbs(v-if="breadcrumbs.length")
      NavItem.breadcrumb(
        v-for="fragment in breadcrumbs" :key="fragment"
        :to="fragment"
      ) {{ fragment }}
    span.center(v-else)
      NavItem Ewen Le Bihan

    NavLanguageSwitch.right
</template>

<script>
import NavItem from '~/components/NavItem.vue'
import NavLanguageSwitch from '~/components/NavLanguageSwitch.vue'
import Iconed from '~/components/Iconed.vue'

export default {
  components: { NavItem, NavLanguageSwitch, Iconed },
  data() {
    return {
      scrolled: false
    }
  },
  computed: {
    backURL() {
      const path = this.$route.path.replace('fr/', '')
      const fragments = path.split('/')
      if (fragments.length <= 1) {
        return false
      } else {
        fragments.pop()
        const backURL = fragments.join('/') // localePath() is handled by <NavItem>
        if (backURL === '/works') {
          return '/'
        } else {
          return backURL
        }
      }
    },
    breadcrumbs() {
      const path = this.$route.path.replace('fr/', '')
      const fragments = path.split('/')
      if (fragments.length <= 2) return []
      fragments.shift()
      fragments.shift()
      let breadcrumbs = []
      fragments.forEach((fragment) => {
        breadcrumbs = [...breadcrumbs, fragment.replace(/-/g, ' ')]
      })
      return breadcrumbs
    }
  },
  mounted() {
    window.addEventListener('scroll', (event) => {
      if (window.scrollY > 100) {
        this.scrolled = true
      } else {
        this.scrolled = false
      }
    })
  }
}
</script>

<style lang="stylus" scoped>
.nav-wrapper
  width 100%
  font-size: 1.5em
  background white
  position fixed
  display flex
  align-items center
  justify-content center
  top 0

nav
  width 100%
  padding 0 20px
  display flex
  align-items center
  .--nav-item:not(:last-child)
    margin-right 1.5em
  .right
    margin-left auto
  .center
    margin 0 auto
  .center.breadcrumbs
    position fixed
    left 50%
    transform translateX(-50%)
  .breadcrumb
    margin-right: 0 !important
  .breadcrumb:not(:last-child)::after
    content '/'
    opacity: 0.25
  .go-back
    border none
</style>
