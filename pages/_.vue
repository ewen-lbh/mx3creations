<template lang="pug">
main
  section(v-if="work")
    Work(v-bind="work")
  section(v-else-if="collection")
    Collection(v-bind="collection")
</template>

<script>
import Work from '~/components/Work.vue'
import Collection from '~/components/Collection.vue'

export default {
  components: { Work, Collection },
  // eslint-disable-next-line handle-callback-err
  asyncData({ error, route, store, app }) {
    const reqPath = route.params.pathMatch.split('/')
    const works = store.getters['works/all']
    const collections = store.getters['works/collections']
    const matchingCollection = collections.find((c) => c.id === reqPath[0])
    let matchingWork
    if (matchingCollection && reqPath.length > 1) {
      matchingWork = works.find((w) => w.id === reqPath[1])
      return {
        collection: matchingCollection,
        work: matchingWork
      }
    } else if (matchingCollection) {
      return {
        collection: matchingCollection,
        work: null
      }
    } else {
      matchingWork = works.find((w) => w.id === reqPath[0])
      if (matchingWork) {
        return {
          work: matchingWork,
          collection: null
        }
      } else {
        error({ message: 'inexistantWork', statusCode: 404 })
      }
    }
    //   const matchingProducts = products.filter(
    //     (p) =>
    //       route.params.id === p.id && route.params.collection === p.collection.id
    //   )
    //   if (matchingProducts.length === 0) {
    //     error({ message: 'inexistantWork', statusCode: 404 })
    //   } else if (matchingProducts.length > 1) {
    //     error({ message: 'internalError', statusCode: 500 })
    //   }
  }
}
</script>
