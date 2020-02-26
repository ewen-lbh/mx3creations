const fs = require('fs')
const chalk = require('chalk')
const yaml = require('yaml')
const Case = require('case')

const parseYAML = (file) => {
  // Handle inexistant files
  if (!fs.existsSync(file)) {
    return new Error(chalk`The file {bold ${file}} does not exist`)
  }
  // Read the file
  let contents = null
  try {
    contents = fs.readFileSync(file).toString()
  } catch (error) {
    return new Error(chalk`Could not read {bold ${file}}`)
  }
  // Parse the file
  try {
    contents = yaml.parse(contents)
    contents = normalizeKeys(contents)
  } catch (error) {
    return new Error(
      chalk`Could not parse {bold ${file}}. Is it a valid YAML file?`
    )
  }
  return contents
}

const normalizeKeys = (object) => {
  const normalized = {}
  Object.entries(object).forEach(([key, value]) => {
    const typeStr = Object.prototype.toString.call(value)
    key = key.replace(' ', '_')
    if (['camel', 'pascal'].includes(Case.of(key))) {
      key = Case.snake(key)
    }
    if (
      value !== null &&
      typeof value === 'object' &&
      typeStr === '[object Object]'
    ) {
      value = normalizeKeys(value)
    }
    normalized[key] = value
  })
  return normalized
}

const getTypeFromExt = (ext) => {
  switch (ext.replace('.', '')) {
    case 'png':
    case 'jpg':
    case 'jpeg':
      return 'image'

    case 'mp4':
      return 'video'

    case 'pdf':
      return 'pdf'

    case 'mp3':
    case 'wav':
    case 'flac':
      return 'audio'

    default:
      return 'text'
  }
}

const getHTMLElementFromExt = (ext) => {
  switch (getTypeFromExt(ext)) {
    case 'video':
      return 'video'
    case 'image':
      return 'img'
    case 'pdf':
      return 'embed'
    case 'text':
      return 'code'
    default:
      return null
  }
}

module.exports = {
  parseYAML,
  getTypeFromExt,
  getHTMLElementFromExt
}
