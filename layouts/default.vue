<template lang="pug">
  .container
    TheNavbar#nav
    .page-container
      nuxt#page
    TheFooter#footer
</template>

<script>
import TheNavbar from '~/components/TheNavbar.vue'
import TheFooter from '~/components/TheFooter.vue'

export default {
  components: { TheNavbar, TheFooter }
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
  min-height 100vh

nav-height = 70px
max-page-width = 1400px
#nav
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
</style>
