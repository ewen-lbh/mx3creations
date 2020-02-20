const products = require('../static/products/database.json')

const processProductHideFrom = (product) => {
  if (product['hide from']) {
    const hideFrom = product['hide from']
    if (['all', '*'].includes(hideFrom)) {
      return ['gallery']
    } else if (typeof product === 'string') {
      return [hideFrom]
    } else if (typeof product === 'object') {
      return hideFrom
    }
  } else {
    return []
  }
}

const processType = (product) => {
  if (product.type) return product.type
  if (product.categories.length === 1) {
    return {
      graphism: 'image',
      motion: 'video',
      software: 'program',
      music: 'audio'
    }[product.categories[0]]
  }
  if (
    product.categories.includes('graphism') &&
    product.categories.includes('music')
  )
    return 'image'
  return null
}

const getProductFrontCover = (product, collection) => {
  const constructURL = (productId, file, ext = 'png') =>
    `http://static.mx3creations.com/renders/${collection.id}/${productId}/${file}.${ext}`
  const frontCover =
    product['front cover'] ||
    product.frontCover ||
    collection['front covers'] ||
    'default'
  let url = null
  const ext = {
    image: 'png',
    video: 'mp4',
    music: 'mp3',
    pdf: 'pdf',
    code: null,
    [null]: 'png'
  }[product.type]
  if (frontCover) {
    if (ext === 'pdf') {
      url = constructURL(product.id, '_thumbnail', 'png')
    } else if (frontCover === 'default') {
      url = constructURL(product.id, product.id, ext)
    } else if (frontCover !== null) {
      url = constructURL(product.id, frontCover, ext)
    }
  }
  return url
}

const flattenProducts = (object, collection) => {
  const flat = []
  if (!object) return []
  Object.entries(object).forEach(([k, v]) => {
    let prod = { ...v, id: k }
    prod = { ...prod, rendersDir: `/products/renders/${collection.id}/${k}/` }
    prod = { ...prod, hideFrom: processProductHideFrom(v) }
    prod = { ...prod, type: processType(v) }
    prod = { ...prod, frontCover: getProductFrontCover(prod, collection) }
    prod = { ...prod, title: `${collection.name}: ${v.name}` }
    flat.push(prod)
  })
  return flat
}

const flatCollections = () => {
  const flatCollections = []
  Object.entries(products).forEach(([key, value]) => {
    const flatProducts = flattenProducts(value.products, { ...value, id: key })
    flatCollections.push({
      ...value,
      products: flatProducts,
      singleProduct: flatProducts.length === 1,
      id: key
    })
  })
  return flatCollections
}

export const state = () => ({
  collections: flatCollections()
})

export const getters = {
  all: ({ collections }) => collections,
  byCategory: (_, { all }) => (category) =>
    all.filter(
      (collection) =>
        collection.products.filter((product) => {
          return product.categories.includes(category)
        }).length > 0
    ),
  products: (_, { all }) => {
    const products = []
    all.forEach((collection) => {
      // Inject the collection's properties (except `products`, duh)
      const coll = { ...collection } // Make a copy since `delete` mutates
      delete coll.products
      collection.products.forEach((product) => {
        products.push({
          ...product,
          collection: coll
        })
      })
    })
    return products
  }
}
