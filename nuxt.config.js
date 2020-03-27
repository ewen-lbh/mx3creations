import axios from 'axios'

export default {
  mode: 'universal',
  /*
   ** Headers of the page
   */
  head: {
    title: '',
    titleTemplate: (titleChunk) => {
      let title = 'Ewen Le Bihan'
      const sep = ' · '
      if (titleChunk) title = titleChunk + sep + title
      return title
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      },
      {
        name: 'msapplication-TileColor',
        content: '#00aba9'
      },
      {
        name: 'theme-color',
        content: '#ffffff'
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Inconsolata:400,700&display=swap&subset=latin-ext' // TODO: Use local font
      },
      {
        rel: 'apple-touch-icon',
        sizes: '180x180',
        href: '/apple-touch-icon.png'
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '32x32',
        href: '/favicon-32x32.png'
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '16x16',
        href: '/favicon-16x16.png'
      },
      {
        rel: 'manifest',
        href: '/site.webmanifest'
      },
      {
        rel: 'mask-icon',
        href: '/safari-pinned-tab.svg',
        color: '#00aba9'
      }
    ]
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: [
    // Global styles
    '~assets/styles/global.styl',
    // Fonts
    '~assets/fonts/RobotoMono/import.css',
    '~assets/fonts/Recursive/import.css',
    '~assets/fonts/work-sans/import.css'
  ],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [],
  /*
   ** Generation settings
   */
  generate: {
    routes() {
      return axios
        .get('https://static.ewen.works/works.json')
        .then(({ data }) => {
          const fullIds = data.map((w) => w.full_id)
          let workAndCollectionsRoutes = []
          fullIds.forEach((id) => {
            const path = id.split('/')
            // A collection-less work
            if (path.length === 1) {
              workAndCollectionsRoutes.push(id)
              // A work that goes into a collection
            } else if (path.length === 2) {
              // Add the work itself
              workAndCollectionsRoutes.push(id)
              // Add the collection itself (we'll worry about duplicates later)
              workAndCollectionsRoutes.push(path[0])
            }
          })
          // Remove duplicates
          workAndCollectionsRoutes = [...new Set(workAndCollectionsRoutes)]
          // Prefix with '/'
          workAndCollectionsRoutes = workAndCollectionsRoutes.map(
            (route) => '/' + route
          )
          const { usingHrefs, tags } = require('./store/constants').state()
          const technologies = Object.keys(usingHrefs)
          const madeWithRoutes = technologies.map(
            (tech) => `/made-with/${tech}`
          )
          const taggedRoutes = tags.map((tag) => `tagged/${tag}`)
          return axios
            .get('https://static.ewen.works/sites.json')
            .then(({ data }) => {
              const redirectsRoutes = Object.entries(data).map(
                ([name]) => `/to/${name}`
              )
              return [
                ...redirectsRoutes,
                ...workAndCollectionsRoutes,
                ...madeWithRoutes,
                ...taggedRoutes
              ]
            })
        })
    }
  },
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module'
    // Doc: https://github.com/nuxt-community/stylelint-module
    // '@nuxtjs/stylelint-module'
  ],
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/pwa',
    // Doc: https://github.com/nuxt-community/dotenv-module
    '@nuxtjs/dotenv',
    'nuxt-i18n',
    // Doc: https://github.com/nuxt-community/modules/tree/master/packages/toast
    '@nuxtjs/toast'
  ],
  /*
   ** nuxt-i18n module configuration
   ** See https://nuxt-community.github.io/nuxt-i18n/
   */
  i18n: {
    locales: [
      // { code: 'en', file: 'en-US.js' },
      { code: 'fr', file: 'fr-FR.js' }
    ],
    defaultLocale: 'fr',
    lazy: true,
    langDir: 'lang/',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'lang'
    }
  },
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {},
  /*
   ** Toast module configuration
   ** See https://www.npmjs.com/package/@nuxtjs/toast
   */
  toast: {
    position: 'bottom-center'
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {
      if (ctx.isDev) {
        config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
      }
    }
  }
}
