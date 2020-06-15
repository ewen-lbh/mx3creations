<template lang="pug">
main
  h1(v-html="$t('aboutPage.whoami')")
  section
    p.intro(v-html="$t('aboutPage.intro')")
  section
    h2(v-html="$t('aboutPage.artistic.heading')")
    p(v-html="$t('aboutPage.artistic.text')")
  section
    h2(v-html="$t('aboutPage.digital.heading')")
    div(v-html="$t('aboutPage.digital.text')")
  section
    h2(v-html="$t('aboutPage.linguistic.heading')")
    p(v-html="$t('aboutPage.linguistic.text')")
  section
    h2(v-html="$t('aboutPage.scientific.heading')")
    p(v-html="$t('aboutPage.scientific.text')")
</template>

<script>
export default {}
</script>

<style lang="stylus" scoped>
main
  margin-top: 20px

main /deep/
  & h1, & h2
    font-family: Work Sans

  & h1
    font-size: 10vmin

  & h2
    font-size: 5vmin
    margin-top: 0.5em
    margin-bottom: 0

  & p
    margin-top: 0
    text-align: justify
</style>
