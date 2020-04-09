<template lang="pug">
  footer
    h2
      svg(v-html="svgLogoContents")
      span ewen-lbh
    p
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
          a(:href="site.url"): Iconed(:icon="site.name" color="var(--prim)") {{ $t(site.name) }}
      ul.music
        h3 Ma musique
        li: a(href="https://open.spotify.com/artist/6tUc6r8aNeiiT1mElcnMx9?si=b5fFKalkTq-WskCj45Xpsg")
          Iconed(icon="spotify" color="var(--prim)") Spotify
    p
      | ∀ work ∈ works
      br
      | work ∈ ewen ⇒ work ∈ creative ∩ digital
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
      ).map(([name, url]) => ({ name, url })),
      svgLogoContents: require(`!raw-loader!@/static/logo.svg`).default
    }
  }
}
</script>

<style lang="stylus" scoped>
footer
  display: flex
  background: var(--text)
  color: var(--prim)
  padding: 20px
  padding-top: 40px
  border-top: 1px solid var(--prim)
  text-align: center
  flex-direction: column
  justify-content: center

h2
  display: flex
  align-items: center
  justify-content: center
  font-family: Work Sans
  font-size: 7.5vmin
  margin: 0
  --fill: var(--prim)

h2 svg
  width: 8vmin
  margin-right: 2vmin

.columns
  display: grid
  max-width: 1000px
  width: 100%
  margin: 0 auto
  grid-gap: 2em
  grid-template-columns: 1fr 1fr 1fr

  @media (max-width: 1000px)
    grid-template-columns: 1fr 1fr

  @media (max-width: 500px)
    grid-template-columns: 1fr

.columns ul
  text-align: left

.columns li
  margin-bottom: 0.5em
  font-size: 1.4em

.columns a:hover
  opacity: 0.75

h3
  font-family: Work Sans
  opacity: 0.5
  font-weight: normal
  border-bottom: 2px solid var(--prim)
  padding-bottom: 7px

.social a
  text-transform: capitalize
</style>
