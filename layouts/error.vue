<template lang="pug">
  main.centered
    h1 {{ error.statusCode }}
    template(v-if="error.statusCode === 404")
      p {{ $t(error.message) || $t('inexistantPage') }}
    template(v-else)
      p Une erreur s'est produite

    BtnOutline(href="/") {{ $t('backToHome') }}
</template>

<script>
import BtnOutline from '~/components/BtnOutline.vue'

export default {
  components: { BtnOutline },
  // eslint-disable-next-line vue/require-prop-types
  props: ['error']
}
</script>

<style lang="stylus" scoped>
h1
  font-size 20vmin
  margin-bottom 0
  animation status-code 0.5s linear infinite alternate
  font-family 'Recursive'

@keyframes status-code
  0%
    font-variation-settings "MONO" 1, "CASL" 0, "wght" 700, "slnt" 0
    transform: scale(1) // skew(0)
  11%
    font-variation-settings "MONO" 1, "CASL" 0, "wght" 700, "slnt" 0
    transform: scale(1.1) // skew(0)
  22%
    font-variation-settings "MONO" 0, "CASL" 0, "wght" 500, "slnt" -15
    transform: scale(1) // skew(80deg)
  33%
    font-variation-settings "MONO" 0, "CASL" 0, "wght" 500, "slnt" 0
    transform: scale(1.3) // skew(0)
  44%
    font-variation-settings "MONO" 0, "CASL" 1, "wght" 300, "slnt" 0
    transform: scale(1) // skew(0)
  55%
    font-variation-settings "MONO" 1, "CASL" 1, "wght" 300, "slnt" -10
    transform: scale(1) // skew(0)
  66%
    font-variation-settings "MONO" 1, "CASL" 1, "wght" 1000, "slnt" 0
    transform: scale(1) // skew(0)
  77%
    font-variation-settings "MONO" 1, "CASL" 1, "wght" 1000, "slnt" 0
    transform: scale(0.8) // skew(80deg)
  88%
    font-variation-settings "MONO" 0, "CASL" 0, "wght" 900, "slnt" 0
    transform: scale(1) // skew(0)
  100%
    font-variation-settings "MONO" 0, "CASL" 0, "wght" 900, "slnt" -15
    transform: scale(1) // skew(0)
</style>
