<template lang="pug">
.loader
  template(v-if="work")
    Work(v-bind="work")
  template(v-else-if="collection")
    Collection(v-bind="collection")
</template>

<script>
import Work from '~/components/Work.vue'
import Collection from '~/components/Collection.vue'

export default {
  components: { Work, Collection },
  asyncData({ error, route, store, app }) {
    const reqPath = route.params.pathMatch.split('/')
    const works = store.getters['works/all']
    const collections = store.getters['works/collections']
    const matchingCollection = collections.find((c) => c.id === reqPath[0])
    let matchingWork
    if (matchingCollection && reqPath.length > 1) {
      matchingWork = works.find(
        (w) => w.full_id === reqPath[0] + '/' + reqPath[1]
      )
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
  },
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
