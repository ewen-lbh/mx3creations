const fs = require('fs')
const path = require('path')
const execa = require('execa')
const _ = require('lodash')

module.exports = {
  getList(ctx) {
    const thumbs = ctx.variants
      .map((v) => {
        const dir = path.resolve(
          ctx.program.args[1],
          v.ids.collection,
          v.ids.product
        )
        const basename = path.basename(v.file, path.extname(v.file))
        let thumbPathIn
        if (v.type === 'image') {
          thumbPathIn = path.resolve(dir, v.file)
        } else if (v.type === 'video') {
          thumbPathIn = path.resolve(
            dir,
            'processed-videos',
            basename + '_poster.jpg'
          )
        } else if (v.type === 'pdf') {
          const thumbPathInDir = path.resolve(dir, 'processed-pdfs')
          thumbPathIn = fs
            .readdirSync(thumbPathInDir)
            .filter(
              (file) => file.includes(v.id) && path.extname(v.id) === 'png'
            )
            .sort()[0]
          if (thumbPathIn === undefined) {
            return null
          }
        } else {
          return null
        }
        const getThumbPathOutDir = (resolution) =>
          path.resolve(dir, 'thumbs', resolution.toString())
        return { ...v, thumbPathIn, getThumbPathOutDir }
      })
      .filter((v) => v !== null)
    const resolutions = [20, 250, 500, 750]
    return _.flatten(
      thumbs.map((v) => {
        let skipped = false
        // See https://github.com/schlosser/pig.js/#step-2-create-a-structure-to-serve-your-images for resolutions
        const resolutionThumbs = []
        for (const resolution of resolutions) {
          const dir = v.getThumbPathOutDir(resolution)
          if (
            fs.existsSync(
              path.resolve(
                dir,
                path.basename(v.file, path.extname(v.file)) + '.png'
              )
            )
          ) {
            skipped = true
          }
          const thumbPathOut = path.resolve(
            dir,
            path.basename(v.file, path.extname(v.file)) + '.png'
          )
          resolutionThumbs.push({
            dir,
            ...v,
            resolution,
            skipped,
            thumbPathOut
          })
        }
        return resolutionThumbs
      })
    )
  },
  makeDirs(thumbs) {
    for (const thumb of thumbs) {
      if (!fs.existsSync(thumb.dir)) {
        fs.mkdirSync(thumb.dir, { recursive: true })
      }
    }
  },
  processOne(thumb) {
    ;(async () =>
      // eslint-disable-next-line no-return-await
      await execa('convert', [
        '-thumbnail',
        thumb.resolution,
        thumb.thumbPathIn,
        thumb.thumbPathOut
      ]))()
  }
}
