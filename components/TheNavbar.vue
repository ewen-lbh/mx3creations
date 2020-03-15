<template lang="pug">
//-TODO: Animate in/out of nav items (back&forth between creations/about/contact & ← go back, ewen le bihan to breadcrumbs)
//-TODO: Animate (swoosh-like motion) current page indicator bar (eg. from CREATIONS to CONTACT), stretch to both then stretch back to dest.
.nav-wrapper(:class="{ scrolled, opened }")
  nav
    // Left
    template(v-if="backURL")
      NavItem.go-back(@click="goBack"): Iconed(icon="arrow-left") {{ $t('back') }}
    template(v-else)
      NavItem(to="/") {{ $t('works') }}
      NavItem(to="/about") {{ $t('about') }}
    // Center
    span.center.breadcrumbs(v-if="false")
      NavItem.breadcrumb(
        v-for="fragment in breadcrumbs" :key="fragment"
        :to="fragment"
        no-line
      ) {{ fragment }}
    nuxt-link(v-else to="/").center
      NavItem Ewen Le Bihan
    NavItem.switch-menu.center(@click="switchMenu") {{ $t(switchMenuText) }}
    // Right
    NavItem.right(to="/contact") {{ $t('contact') }}
</template>

<script>
import NavItem from '~/components/NavItem.vue'
import NavLanguageSwitch from '~/components/NavLanguageSwitch.vue'
import Iconed from '~/components/Iconed.vue'

export default {
  components: { NavItem, NavLanguageSwitch, Iconed },
  data() {
    return {
      scrolled: false,
      opened: false
    }
  },
  computed: {
    switchMenuText() {
      return this.opened ? 'closeMenu' : 'openMenu'
    },
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
      // TODO: Rework this. Disabled for now
      const path = this.$route.path.replace('fr/', '')
      const fragments = path.split('/')
      if (fragments.length <= 1) return []
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
  },
  methods: {
    switchMenu() {
      this.opened = !this.opened
      if (this.opened) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = 'auto'
      }
    },
    goBack() {
      history.go(-1)
    }
  }
}
</script>

<style lang="stylus" scoped>
.nav-wrapper
  width 100%
  font-size: 1.5em
  background transparent
  position fixed
  display flex
  align-items center
  justify-content center
  top 0  box-sizing border-box
  transition all 0.5s ease, border 0.25s ease
  border 2px solid transparent
  z-index: 1000

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
  position: fixed
  left: 50%
  transform: translateX(-50%)

.breadcrumb
  margin-right: 0 !important
.breadcrumb:not(:last-child)::after
  content '/'
  opacity: 0.25
.go-back
  border none
.switch-menu
  display none
  position fixed
  bottom: 16px
  left 50%
  transform translateX(-50%)
  z-index: 1010

@media (max-width 900px)
  .center:not(.switch-menu)
    display none

@media (max-width 600px)
  .nav-wrapper
    bottom: 0
    top unset
    border-top-color var(--text)
    background var(--prim)

@media (max-width 400px)
  .switch-menu
    display inline-block
  .--nav-item:not(.switch-menu)
    display none

.opened
  bottom: 0
  left: 0
  right: 0
  z-index: 1000
  height 100vh
  border-color black
  align-items flex-end
  nav
    flex-direction column
    justify-content flex-end
    align-items flex-start
    margin-bottom: 100px
  .--nav-item
    display block
    margin-right: 0
    margin-left: 0
  .--nav-item:not(:last-child):not(.switch-menu)
    margin-bottom .5em

.scrolled
  .center:not(.switch-menu)
    opacity 0
    pointer-events none
</style>
