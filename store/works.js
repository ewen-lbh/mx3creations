const bestWorksIDs = require('../static/best-works-ids.json')

export const state = () => ({
  works: require('../static/works.json')
})

export const getters = {
  all: ({ works }) =>
    works.map((w) => ({
      ...w,
      best: bestWorksIDs.includes(w.id)
    })),
  best: (_, { all }) => all.filter((w) => w.best),
  byID: (_, { all }) => (id) => all.find((w) => w.id === id)
}
