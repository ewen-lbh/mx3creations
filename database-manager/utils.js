const fs = require('fs')
const ora = require('ora')
const boxen = require('boxen')
const chalk = require('chalk')
const yaml = require('yaml')
const Case = require('case')

const parseYAML = (file) => {
  const spinner = ora('Loading database...').start()
  // Handle inexistant files
  spinner.text = chalk`Checking if {bold ${file}} exists...`
  if (!fs.existsSync(file)) {
    spinner.fail(chalk`The file {bold ${file}} does not exist`)
    process.exit(1)
  }
  // Read the file
  spinner.text = chalk`Reading {bold ${file}}...`
  let contents = null
  try {
    contents = fs.readFileSync(file).toString()
  } catch (error) {
    spinner.faill(chalk`Could not read {bold ${file}}`)
    console.log(boxen(error, { borderStyle: 'round' }))
    process.exit(1)
  } finally {
    // Parse the file
    try {
      spinner.text = chalk`Parsing {bold ${file}}...`
      contents = yaml.parse(contents)
      spinner.text = chalk`Normalizing keys...`
      contents = normalizeKeys(contents)

      const collectionsCount = Object.keys(contents).length
      spinner.succeed(
        chalk`Loaded {green {bold ${collectionsCount}}} collections from {bold ${file}}`
      )
    } catch (error) {
      spinner.fail(
        chalk`Could not parse {bold ${file}}. Is it a valid YAML file?`
      )
      console.log(
        boxen(chalk`{red ${error}}`, {
          padding: 1,
          margin: 1,
          borderStyle: 'round',
          borderColor: 'red'
        })
      )
      process.exit(1)
    }
  }
  return contents
}

const normalizeKeys = (object) => {
  const normalized = {}
  Object.entries(object).forEach(([key, value]) => {
    const typeStr = Object.prototype.toString.call(object)
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

module.exports = {
  parseYAML
}
