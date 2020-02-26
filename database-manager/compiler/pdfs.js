const fs = require('fs')
const path = require('path')
const execa = require('execa')
const program = require('commander')

module.exports = {
  getList(ctx) {
    const pdfs = ctx.variants
      .filter((variant) => variant.type === 'pdf')
      .map((pdf) => {
        const dir = path.resolve(
          program.args[1],
          pdf.ids.collection,
          pdf.ids.product
        )
        return {
          absPath: path.resolve(dir, pdf.file),
          outDir: path.resolve(dir, 'processed-pdfs'),
          fileNoExt: path.basename(pdf.file, path.extname(pdf.file)),
          ...pdf
        }
      })
    return pdfs
  },
  processOne(pdf) {
    if (!fs.existsSync(pdf.outDir)) {
      fs.mkdirSync(pdf.outDir)
    }
    return execa('pdftoppm', [
      pdf.absPath,
      path.join(pdf.outDir, pdf.fileNoExt),
      '-png'
    ])
  }
}
