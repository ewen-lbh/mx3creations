<template lang="pug">
  footer
    h2 ewen.works
    p
      | En cours de développement
      br
      | Fait avec ❤ par Ewen Le Bihan, aka Mx3
      br
      | Fièrement #[em non] propulsé par WordPress
      br
      BtnOutline(inverted small href="https://github.com/ewen-lbh/mx3creations" target="_blank") Code source
    .columns
      ul.links
        h3 Liens
        li: nuxt-link(:to="localePath('/')") {{ $t('works') }}
        li: nuxt-link(:to="localePath('/about')") {{ $t('about') }}
        li: nuxt-link(:to="localePath('/contact')") {{ $t('contact') }}
        li: nuxt-link(:to="localePath('/legal')") {{ $t('legal') }}
        li: nuxt-link(:to="localePath('/credits')") {{ $t('credits') }}
      ul.social
        h3 Sur les réseaux
        li(v-for="site in sites")
          Iconed(:icon="site.name"): a(:href="site.url") {{ $t(site.name) }}
      ul.music
        h3 Ma musique
        li: a(href="https://open.spotify.com/artist/4jUrQ2TvXDA6Nupa9NBVcI?si=PIYJsVMPQHqOPDmXnNdVug") Spotify
        li: a(href="https://www.deezer.com/fr/artist/12928429") Deezer
</template>

<script>
import BtnOutline from '~/components/BtnOutline.vue'
import Iconed from '~/components/Iconed.vue'

export default {
  components: { BtnOutline, Iconed },
  data() {
    return {
      sites: Object.entries(
        require('static/sites.json')
      ).map(([name, url]) => ({ name, url }))
    }
  }
}
</script>

<style lang="stylus" scoped>
footer
  display flex
  background var(--text)
  color var(--prim)
  padding 20px
  padding-top: 40px
  border-top 1px solid var(--prim)
  text-align center
  flex-direction column
  justify-content center
h2
  font-family Work Sans
  font-size 7.5vmin
  margin: 0
.columns
  display grid
  max-width 1000px
  width 100%
  margin 0 auto
  grid-gap 2em
  grid-template-columns 1fr 1fr 1fr
  @media (max-width 1000px)
    grid-template-columns 1fr 1fr
  @media (max-width 500px)
    grid-template-columns 1fr
.columns ul
  text-align left
.columns li
  margin-bottom .5em
.columns a:hover
  opacity .75
h3
  font-family Work Sans
  opacity: 0.5
  font-weight normal
  border-bottom 2px solid var(--prim)
  padding-bottom: 7px

.social a
  text-transform capitalize
</style>
