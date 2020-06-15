<template lang="pug">
main
  h1 {{ $t('madeInPage.heading').replace(/%years%/, yearsListDisplay) }}
  Gallery(:works="worksOfYears")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'

export default {
  components: { Gallery },
  computed: {
    ...mapGetters('works', ['all']),
    worksOfYears() {
      let filtered = []
      this.years.forEach((y) => {
        filtered = [...filtered, ...this.all.filter((p) => p.year === y)]
      })
      return filtered
    },
    urlParam() {
      return this.$route.params.years
    },
    years() {
      return this.urlParam.split(',').map((y) => Number(y))
    },
    yearsListDisplay() {
      return this.years.join(', ').replace(/, ([^,]*)$/, ' et en $1')
    }
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-family: Work Sans
  font-size: max(10vmin, 2rem)
  margin-bottom: 0.25em
  text-align: center
  margin: 0
  margin-bottom: 1rem

  a
    transition: opacity 0.25s ease
    border-bottom: 0.0625em dotted rgba(0, 0, 0, 0.25)

  a:hover
    opacity: 0.25

.--years-list
  display: flex
  justify-content: center
</style>
