export const state = () => ({
  collections: require('../static/products/database.json')
})

export const getters = {
  collections: ({ collections }) => collections,
  collectionByCategory: (_, { collections }) => (category) =>
    collections.filter(
      (collection) =>
        collection.products.filter((product) => {
          return product.categories.includes(category)
        }).length > 0
    ),
  products: (_, { collections }) => {
    let products = []
    collections.forEach((collection) => {
      products = [...products, ...collection.products]
    })
    return products
  }
}
