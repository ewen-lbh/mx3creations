<template lang="pug">
main
  h1 {{$t('contactPage.heading')}}
  dl
    dt {{$t('contactPage.byEmail')}}
    dd: a(href="mailto:ewen.lebihan7@gmail.com") ewen.lebihan7@gmail.com

    dt {{$t('contactPage.byTwitter')}}
    dd(v-html="$t('contactPage.sendDMTo')")
</template>

<style lang="stylus" scoped>
dl
  max-width 500px
  margin 0 auto
  font-size: 1.2em
  dt
    font-size: 1.3em
    margin-top 1em
</style>
