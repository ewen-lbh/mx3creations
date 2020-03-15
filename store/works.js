export const state = () => ({
  works: require('../static/works.json')
})

export const getters = {
  all: ({ works }) => works,
  bestOf: () => (works) => works.filter((w) => w.best),
  best: (_, { all, bestOf }) => bestOf(all),
  byID: (_, { all }) => (id) => all.find((w) => w.id === id),
  ofFirstTag: (_, { all }) => (tag) =>
    all.filter((w) => w.tags && w.tags[0] === tag),
  withTags: (_, { all }) => (tags) => {
    const result = []
    tags.forEach((tag) => {
      result.push(all.filter((w) => w.tags && w.tags.includes(tag)))
    })
    return result
  },
  collections: (_, { all }) =>
    all.filter((w) => w.collection).map((w) => w.collection),
  ofCollection: (_, { all }) => (collectionID) =>
    all.filter((w) => w.collection && w.collection.id === collectionID)
}
