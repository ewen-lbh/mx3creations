<template lang="pug">
  .container
    LocalhostWarning
    TheNavbar#nav
    .page-container
      nuxt#page
    TheFooter#footer
    script(async defer src="https://scripts.simpleanalyticscdn.com/latest.js")
    noscript: img(src="https://queue.simpleanalyticscdn.com/noscript.gif" alt="")
</template>

<script>
import TheNavbar from '~/components/TheNavbar.vue'
import TheFooter from '~/components/TheFooter.vue'
import LocalhostWarning from '~/components/LocalhostWarning.vue'

export default {
  components: { TheNavbar, TheFooter, LocalhostWarning }
}
</script>

<style lang="stylus" scoped>
body
  display flex
  flex-direction column

#page.centered
  display flex
  justify-content center
  align-items center
  flex-direction column
  min-height calc(100vh - 90px) //ref:computed:<TheNavbar>/height

#page
  padding 0 20px

nav-height = 70px
max-page-width = 1400px
#nav:not(.opened)
  height nav-height
  & /deep/ nav
    max-width max-page-width
#page
  margin-top nav-height
  max-width max-page-width
.page-container
  display flex
  justify-content center

#page .gallery
  margin-bottom: 40px

#footer
  margin-top: 100px
  padding-bottom: 70px
</style>
