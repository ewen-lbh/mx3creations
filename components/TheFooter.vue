<template lang="pug">
  footer
    .langage-switcher
      nuxt-link(
        :to="switchLocalePath('en')"
        :class="{ current:  $i18n.locale === 'en' }"
      ) English
      span.sep /
      nuxt-link(
        :to="switchLocalePath('fr')"
        :class="{ current:  $i18n.locale === 'fr' }"
      ) Français
</template>

<style lang="stylus" scoped>
footer
  display flex
  justify-content center
  background black
  color white
  height: 100px
  padding 20px
  padding-top: 40px
  border-top 1px solid white

.langage-switcher
  text-transform uppercase
  font-size 1.5em
  a
    transition all .5s ease
  a:hover
    font-weight bold
  a.current
    opacity: 0.5
  .sep
    opacity: 0.5
    // font-weight bold
</style>
