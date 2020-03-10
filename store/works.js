const bestWorksIDs = require('../static/best-works-ids.json')

export const state = () => ({
  works: require('../static/works.json')
})

export const getters = {
  all: ({ works }) =>
    works.map((w) => ({
      ...w,
      best: w.collection
        ? bestWorksIDs.includes(w.collection.id)
        : bestWorksIDs.includes(w.id)
    })),
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
  }
}
