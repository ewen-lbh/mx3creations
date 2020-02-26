const fs = require('fs')
const path = require('path')
const program = require('commander')
const _ = require('lodash')
const sizeOf = require('image-size')
const utils = require('../utils')

module.exports = {
  load(ctx) {
    ctx.database = utils.parseYAML(ctx.program.args[0])
    return ctx
  },
  compile(ctx) {
    ctx.collections = []
    Object.entries(ctx.database).forEach(([collectionID, collection]) => {
      // Push a new collection
      ctx.collections.push({
        // ID
        id: collectionID,
        // Directory of renders
        renders_dir: path.relative(
          '../static/',
          path.resolve(program.args[1], collectionID)
        ),
        // Remove spaces from tags & categories
        tags:
          collection.tags && collection.tags.map((t) => t.replace(/ /g, '-')),
        categories:
          collection.categories &&
          collection.categories.map((t) => t.replace(/ /g, '-')),
        // Normal properties
        ...collection,
        // Flattened products list
        products: Object.entries(collection.products).map(
          ([productID, product]) => {
            //
            const variantsDir = path.resolve(
              program.args[1],
              collectionID,
              productID
            )
            if (!fs.existsSync(variantsDir)) return
            const variantsFiles = fs
              .readdirSync(variantsDir)
              .filter((item) =>
                fs.statSync(path.resolve(variantsDir, item)).isFile()
              )
            const isFrontCover = (file) =>
              path.basename(file, path.extname(file)) === String(frontCover)
            const getVariantSrc = (file) =>
              (program.local ? '' : 'http://static.mx3creations.com') +
              '/' +
              path.relative('../static', path.join(variantsDir, file))
            const getVariantObject = (file) => {
              const variantID = path.basename(file, path.extname(file))
              let obj = {
                file,
                type: utils.getTypeFromExt(path.extname(file)),
                html_element: utils.getHTMLElementFromExt(path.extname(file)),
                src: getVariantSrc(file),
                resolutionSrc: path.join(getVariantSrc('{size}'), file),
                gid: `${collectionID}:${productID}:${
                  variantID === productID ? ':' : variantID
                }`,
                ids: {
                  collection: collectionID,
                  product: productID,
                  variant: variantID
                }
              }
              if (obj.type === 'text') {
                obj = {
                  ...obj,
                  content: fs
                    .readFileSync(path.resolve(variantsDir, file))
                    .toString()
                }
              } else {
                obj = { ...obj, content: null }
              }
              if (obj.type === 'image') {
                const { height, width } = sizeOf(
                  path.resolve(variantsDir, file)
                )
                obj = {
                  ...obj,
                  size: {
                    height,
                    width,
                    aspect_ratio: width / height
                  }
                }
              }
              return obj
            }
            const frontCover =
              product['front cover'] || collection['front covers'] || productID
            return {
              ...product,
              id: productID,
              gid: `${collectionID}:${productID}`,
              title: `${collection.name}: ${product.name}`,
              hide_from: product.hide_from || [],
              front_cover:
                variantsFiles
                  .filter((file) => isFrontCover(file))
                  .map((file) => getVariantObject(file))[0] ||
                getVariantObject(variantsFiles[0]),
              variants: variantsFiles.map((file) => getVariantObject(file)),
              collection: Object.keys(collection)
                .filter((k) => k !== 'products')
                .reduce(
                  (acc, cur) => ({
                    ...acc,
                    [cur]: collection[cur],
                    id: collectionID
                  }),
                  {}
                )
            }
          }
        )
      })
    })
    ctx.collections = ctx.collections.map((c) => ({
      ...c,
      products: c.products.filter((p) => p !== null && p !== undefined)
    }))
    ctx.products = _.flatten(ctx.collections.map((c) => c.products))
    ctx.variants = _.flatten(ctx.products.map((p) => p.variants))
    return ctx
  },
  write(ctx) {
    const jsoned = JSON.stringify(ctx.collections, null, program.indentation)

    const outputFile =
      ctx.program.output ||
      ctx.program.args[0].replace(/\.ya?ml$/, ($0) => '.json')
    fs.writeFileSync(outputFile, jsoned)
  }
}
