<template lang="pug">
  main(v-html="$t('html.about')")
</template>

<style lang="stylus" scoped>
main
  margin-top: 20px

main /deep/
  & h1, & h2
    font-family Work Sans
  & h1
    font-size 10vmin
  & h2
    font-size 5vmin
    margin-top: 0.5em
    margin-bottom: 0
  & p
    margin-top: 0
    text-align justify
</style>
