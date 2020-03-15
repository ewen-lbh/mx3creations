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
        li: Iconed(icon="youtube"): a(href="//youtube.com/c/mx3_music") YouTube
        li: Iconed(icon="twitter"): a(href="//twitter.com/mx3_fr") Twitter
        li: Iconed(icon="instagram"): a(href="//instagram.com/mx3_fr") Instagram
        li: Iconed(icon="facebook"): a(href="//facebook.com/mx3fr") Facebook
        li: Iconed(icon="discord"): a(href="//discord.gg/a2Yqd3j") Discord
        li: Iconed(icon="reddit"): a(href="//reddit.com/r/mx3") Reddit
      ul.music
        h3 Ma musique
        li: a(href="https://open.spotify.com/artist/4jUrQ2TvXDA6Nupa9NBVcI?si=PIYJsVMPQHqOPDmXnNdVug") Spotify
        li: a(href="https://www.deezer.com/fr/artist/12928429") Deezer
</template>

<script>
import BtnOutline from '~/components/BtnOutline.vue'
import Iconed from '~/components/Iconed.vue'

export default {
  components: { BtnOutline, Iconed }
}
</script>

<style lang="stylus" scoped>
footer
  display flex
  background black
  color white
  padding 20px
  padding-top: 40px
  border-top 1px solid white
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
  border-bottom 2px solid white
  padding-bottom: 7px
</style>
