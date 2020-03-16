export const state = () => ({
  works: [],
  loaded: false
})

export const mutations = {
  SET: (state, works) => (state.works = works),
  POSTLOAD: (state) => (state.loaded = true)
}

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
    all.filter((w) => w.collection && w.collection.id === collectionID),
  usingList: (_, { all }) => {
    const usings = []
    all.forEach((w) => {
      usings.push(...w.using)
    })
    return [...new Set(usings)]
  }
}

export const actions = {
  async load({ commit, state }, { force } = { force: false }) {
    if (!force && state.loaded) return
    try {
      let works
      if (process.env.NODE_ENV === 'production') {
        const { data } = await this.$axios.get(
          'http://static.mx3creations.com/works.json'
        )
        works = data
      } else {
        works = require('@/static/works.json')
      }
      if (works) {
        commit('SET', works)
        commit('POSTLOAD')
      }
    } catch (error) {}
  }
}
