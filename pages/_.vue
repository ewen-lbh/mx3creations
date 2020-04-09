<template lang="pug">
.loader
  template(v-if="work")
    Work(v-bind="work")
  template(v-else-if="collection")
    Collection(v-bind="collection")
  template(v-else-if="allWorks")
    h1 Toutes mes créations
    Gallery(:works="all")
</template>

<script>
import { mapGetters } from 'vuex'
import Gallery from '~/components/Gallery.vue'
import Work from '~/components/Work.vue'
import Collection from '~/components/Collection.vue'

export default {
  components: { Work, Collection, Gallery },
  asyncData({ error, route, store, app, redirect }) {
    const reqPath = route.params.pathMatch.split('/')
    const works = store.getters['works/all']
    const collections = store.getters['works/collections']
    const matchingCollection = collections.find((c) => c.id === reqPath[0])
    let matchingWork
    if (reqPath[0] === 'all') {
      return { allWorks: true }
    }
    if (matchingCollection && reqPath.length > 1) {
      matchingWork = works.find(
        (w) => w.full_id === reqPath[0] + '/' + reqPath[1]
      )
      return {
        collection: matchingCollection,
        work: matchingWork
      }
    }
    if (matchingCollection) {
      return {
        collection: matchingCollection,
        work: null
      }
    }
    matchingWork = works.find((w) => w.id === reqPath[0])
    if (matchingWork) {
      return {
        work: matchingWork,
        collection: null
      }
    }
    const tags = Object.keys(require('@/lang/fr-FR').default.tags.singular)

    if (tags.includes(route.params.pathMatch)) {
      redirect(`/tagged/${reqPath}`)
    } else {
      error({ message: 'inexistantWork', statusCode: 404 })
    }
  },
  computed: mapGetters('works', ['all']),
  head() {
    let title = ''
    if (this.collection) {
      title += this.collection.name
    }
    if (this.collection && this.work) {
      title += ': '
    }
    if (this.work) {
      title += this.work.name
    }
    return {
      title
    }
  }
}
</script>

<style lang="stylus" scoped>
#page
  flex-grow 1
h1
  font-family Work Sans
  font-size max(10vmin, 3rem)
  margin-bottom .25em
</style>
