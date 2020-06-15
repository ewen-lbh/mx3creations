<template lang="pug">
main
  template(v-if="technologies.length === 1")
    h1
      | {{$t('madeWithPage.heading')}}
      a(
        :href="usingHrefs[technologies[0]]"
        target="_blank"
      ) {{ $t(technologies[0]) }}
  template(v-else)
    h1 {{$t('madeWithPage.heading').replace(/ $/, '…')}}
    TechnologiesList(
      :technologies="technologies"
      :get-url="(tech) => usingHrefs[tech]"
      open-in-new-tab
    )
  Gallery(:works="worksOfTechs")
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import Gallery from '~/components/Gallery.vue'
import TechnologiesList from '~/components/TechnologiesList.vue'

export default {
  components: { Gallery, TechnologiesList },
  computed: {
    ...mapGetters('works', ['all']),
    ...mapState('constants', ['usingHrefs']),
    worksOfTechs() {
      let filtered = []
      this.$route.params.technologies.split(',').forEach((t) => {
        filtered = [...filtered, ...this.all.filter((p) => p.using.includes(t))]
      })
      return filtered
    },
    technologies() {
      return this.$route.params.technologies.split(',')
    }
  }
}
</script>

<style lang="stylus" scoped>
h1
  font-family Work Sans
  font-size max(10vmin, 2rem)
  margin-bottom .25em
  text-align: center
  margin: 0
  a
    transition opacity 0.25s ease
    border-bottom .0625em dotted rgba(0,0,0,0.25)
  a:hover
    opacity: 0.25

.--technologies-list
  display: flex
  justify-content: center
</style>
