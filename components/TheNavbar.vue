<template lang="pug">
.nav-wrapper
  nav(:class="{ scrolled }").desktop-nav
    .nav-group.works
      //- span.nav-item {{ $t('works') }} = {
      nuxt-link.nav-link(
        :to="localePath('/')"
        :class="{current: isCurrent('/')}"
      ) {{ $t('all') }}
      nuxt-link.nav-link(
        v-for="link in links.works"
        :to="localePath(link)"
        :class="{current: isCurrent(link)}"
      ) {{ $t(link.replace('/', '')) }}
      //- span.nav-item.chomp-left-margin }

    //- .nav-group.title
    //-   nuxt-link.nav-link(:to="localePath('/')") Mx3's Creations

    .nav-group.others
      nuxt-link.nav-link(
        v-for="link in links.others"
        :to="localePath(link)"
        :class="{current: isCurrent(link)}"
      ) {{ $t(link.replace('/', '')) }}

  nav.mobile-nav
    nuxt-link.nav-link(
      :class="{current: isCurrent('/')}"
      :to="localePath('/')"
    ) {{ $t('works') }}
    nuxt-link.nav-link(
      :class="{current: isCurrent('/about')}"
      :to="localePath('/about')"
    ) {{ $t('about') }}
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapState, mapGetters } from 'vuex'

export default {
  data() {
    return {
      scrolled: false
    }
  },
  computed: {
    ...mapState('navigation', ['links'])
  },
  methods: {
    isCurrent(link) {
      if (process.browser) {
        const topPathFragment = this.$route.path
          .replace('fr/', '')
          .split('/')[1]
        if (!link.startsWith('/')) link = '/' + link
        return '/' + topPathFragment === link
      }
    }
  },
  mounted() {
    window.addEventListener('scroll', (event) => {
      if (window.scrollY > 0) {
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

nav
  width: 100%
  font-size: 1.5em
  display: flex
  align-items: center
  // background: transparent
  color white

nav.desktop-nav
  padding: 20px 0 // ref:globals.styl/#page/padding
  border-bottom: 1px solid transparent

  &.scrolled
    border-color: white

nav.mobile-nav
  padding: 20px 0 // ref:globals.styl/#page/padding
  border-top: 1px solid white
  display: flex
  justify-content: center
  align-items: center

.nav-link, .nav-item
  transition: all 0.25s ease
  display: flex
  align-items: center
  text-transform: uppercase
  text-decoration: none
  color: inherit

.chomp-left-margin
    margin-left: -1em

.nav-link:not(:last-child)
    margin-right: 1em

.nav-group:not(.title)
  .nav-item
    opacity: 0.5

  .nav-link:hover
    font-weight: 600

.nav-group:not(.title), .mobile-nav
  .nav-link.current
    text-shadow 0 0 1em white, 0 0 .25em white, 0 0 .5em white, 0 0 .75em white, 0 0 1.75em white, 0 0 3em white

.nav-group
  display: flex
  align-items: center

  &.works
    margin-left: 20px // ref:globals.styl/#page/padding

  &.title
    margin: 0 auto

  &.others
    margin-left: auto
    margin-right: 20px // ref:globals.styl/#page/padding

@media (max-width: 1100px)
  nav.desktop-nav
    display: none
  .nav-wrapper
    position fixed
    bottom: 0

@media (min-width: 1101px)
  nav.mobile-nav
    display: none
  .nav-wrapper
    position sticky
    top: 0
</style>
