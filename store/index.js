export const actions = {
  async nuxtServerInit({ dispatch }, _) {
    await dispatch('works/load', { force: true })
  }
}
