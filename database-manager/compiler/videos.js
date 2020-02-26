const fs = require('fs')
const path = require('path')
const WebVideos = require('web-videos')

module.exports = {
  getList(ctx) {
    ctx.videos = ctx.variants
      .filter((v) => v.type === 'video')
      .map((video) => {
        const dir = path.resolve(
          ctx.program.args[1],
          video.ids.collection,
          video.ids.product
        )
        const outDir = path.resolve(dir, 'processed-videos')
        if (!fs.existsSync(outDir)) {
          fs.mkdirSync(outDir)
        }
        const absPath = path.resolve(dir, video.file)
        const posterFormat = {
          format: 'poster',
          time: 2,
          quality: 1
        }
        const gifFormat = {
          format: 'gif',
          fps: 15,
          loop: true,
          bin: `ffmpeg -t 10`
        }
        const posterOutPath = path.resolve(
          outDir,
          `${video.ids.variant}_poster.jpg`
        )
        const gifOutPath = path.resolve(outDir, `${video.ids.variant}.gif`)
        return {
          ...video,
          posterOutPath,
          gifFormat,
          gifOutPath,
          absPath,
          posterFormat,
          dir,
          outDir
        }
      })
    return ctx
  },
  async processOne(ctx, video) {
    await new WebVideos(video.absPath, {
      output_dir: video.outDir,
      temp_dir: './web-videos-temp',
      filename: video.ids.variant,
      formats: [video.gifFormat, video.posterFormat]
    })
  },
  alreadyExists(video) {
    return fs.existsSync(video.posterOutPath) && fs.existsSync(video.gifOutPath)
  }
}
