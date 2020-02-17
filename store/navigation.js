export const state = () => ({
  links: {
    works: ['graphism', 'software', 'music', 'motion'],
    others: ['about', 'contact']
  }
})

export const getters = {
  isCurrent: () => (link) => {
    const topPathFragment = this.$route.path.split('/')[1]
    return '/' + topPathFragment === link
  }
}
