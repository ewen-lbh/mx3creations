export default {
  mode: 'universal',
  /*
   ** Headers of the page
   */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Inconsolata:400,700&display=swap&subset=latin-ext' // TODO: Use local font
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
    'nuxt-i18n'
  ],
  /*
   ** nuxt-i18n module configuration
   ** See https://nuxt-community.github.io/nuxt-i18n/
   */
  i18n: {
    locales: [
      { code: 'en', file: 'en-US.js' },
      { code: 'fr', file: 'fr-FR.js' }
    ],
    defaultLocale: 'en',
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
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {}
  }
}
