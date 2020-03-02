<template lang="pug">
main
  section.left
    .variant(v-for="(variant, i) in product.variants")
      pre.variant-element(v-if="variant.type === 'text'") {{ variant.content }}
      component.variant-element(
        v-else
        :key="variant.gid"
        :is="variant.html_element"
        :src="variant.src"
        :data-aspect-ratio="variant.size.aspect_ratio"
        controls
      )
      h3.text(v-if="product.variants.length > 1")
        template(v-if="showFileName(variant)")
          span.variant-name {{ splitExt(variant.file)[0] }}
          span.variant-ext .{{ splitExt(variant.file)[1] }}
        span.variant-index {{ variantNumber(i) }}
  section.right
    nuxt-link(:to="localePath(`/${product.collection.id}`)")
      h2.collection-name(v-html="product.collection.name")
    h1.product-name(v-html="product.name")
    p.description(v-html="product.description")
    span.categories-overline {{ $t('in') }}
    ul.categories
      li(v-for="(category, i) in product.categories" :key="i")
        nuxt-link(:to="localePath(`/categories/${category}`)") {{ $t('categories.' + category) === `categories.${category}` ? category : $t('categories.' + category) }}
    span.tags-overline {{ $t('tags') }}
    ul.tags
      li(v-for="(tag, i) in product.tags" :key="i")
        nuxt-link(:to="localePath(`/tags/${tag}`)") \#{{ $t('tags.' + tag) === `tags.${tag}` ? tag : $t('tags.' + tag) }}
    template(v-if="product.links")
      h2.see-in-action {{ $t('seeInAction') }}
      ul.links
        li(v-for="(link, i) in product.links" :key="i")
          BtnOutline(:href="link.url || link" target="_blank") {{ link.name || domainName(link) }}
</template>

<script>
import { mapGetters } from 'vuex'
import BtnOutline from '~/components/BtnOutline.vue'

export default {
  components: { BtnOutline },
  fetch({ error, route, store, app }) {
    const products = store.getters['products/products']
    const matchingProducts = products.filter(
      (p) =>
        route.params.id === p.id && route.params.collection === p.collection.id
    )
    if (matchingProducts.length === 0) {
      error({ message: 'inexistantWork', statusCode: 404 })
    } else if (matchingProducts.length > 1) {
      error({ message: 'internalError', statusCode: 500 })
    }
  },
  computed: {
    ...mapGetters('products', ['products', 'all']),
    product() {
      return this.products.find(
        (p) =>
          this.$route.params.id === p.id &&
          this.$route.params.collection === p.collection.id
      )
    },
    collection() {
      return this.product.collection
    },
    frontCoverHTMLElement() {
      switch (this.product.type) {
        case 'image':
        case 'pdf':
          return 'img'

        case 'video':
          return 'video'
      }
      return null
    }
  },
  mounted() {
    document.documentElement.style.setProperty('--bg', 'white')
    document.documentElement.style.setProperty('--bgi', 'black')
    document.documentElement.style.setProperty('--fg', 'black')
    // Set height of images to prevent jankiness
    document.querySelectorAll('.variant-element').forEach((el) => {
      const ratio = parseFloat(el.dataset.aspectRatio)
      const { width } = el.parentElement.getBoundingClientRect()
      const expectedHeight = (1 / ratio) * width
      console.table({ ratio, width, expectedHeight })
      el.style.height = expectedHeight + 'px'
      el.addEventListener('load', (ev) => {
        el.style.height = ''
      })
    })
  },
  methods: {
    domainName(url) {
      let hostname
      // find & remove protocol (http, ftp, etc.) and get hostname
      if (url.includes('//')) {
        hostname = url.split('/')[2]
      } else {
        hostname = url.split('/')[0]
      }

      // find & remove port number
      hostname = hostname.split(':')[0]
      // find & remove "?"
      hostname = hostname.split('?')[0]
      // find & remove "www."
      hostname = hostname.replace('www.', '')

      return hostname
    },
    splitExt(file) {
      return file.split('.')
    },
    showFileName(variant) {
      const name = this.splitExt(variant.file)[0]
      return name !== parseInt(name).toString()
    },
    variantNumber(i) {
      const numLength = Math.ceil(this.product.variants.length / 10) + 1
      return (i + 1).toString().padStart(numLength, '0')
    }
  }
}
</script>

<style lang="stylus" scoped>
//
// Definitions
//
main
  display flex
  align-items flex-start
  flex-direction column
  width 100%
  background-color var(--bg)
  color var(--bgi)
  display: grid
  grid-template-columns 50% 50%
  grid-gap: 3em

img
video
  width 100%

.product-name
  font-size 10vmin //TODO: Scale down to fit text length, target max fontsize=80px
  font-family Work Sans, sans-serif
  letter-spacing: -0.025em
  margin-top: -6vmin
  color var(--bgi)
  text-align left
  line-height: 0.7

.collection-name
  margin-bottom 7.5vmin

section.right
  position sticky
  top: 60px
  margin-left: 0
section.left
  max-width unset
  width: 100%

.see-in-action
  margin-top 2em
  &::before
    thickness = 0.125em
    content ''
    width: 5em
    height: thickness
    background #000
    position absolute
    border-radius thickness / 2
    transform translateY(-5px)

.links
  display flex
  align-items center
  .--btn-outline
    margin-top: 0
    margin-bottom: 0
    margin-left: 0

.variant
  width 100%

.variant-element
  width 100%
  border 1px solid black
.variant:not(:last-child)
  margin-bottom 4em
pre.variant-element
  padding: 10px
  white-space pre-wrap
embed.variant-element
  width 100%

h3
  text-transform uppercase
  font-weight normal
  margin-top: 0
  font-size 1.5em
  width 100%
  display flex

.variant-index
  margin-left auto
  opacity: 0.5
.variant-ext
  opacity: 0.25

.categories
.tags
  margin: 0
  display flex
  align-items center
  li:not(:last-child)
    margin-right: 0.5em
[class$=-overline]
  display block
  margin-top 2em
  margin-bottom: 0.1em
  opacity: 0.5

.tags li
  text-transform lowercase
.categories li
  text-transform uppercase
  font-weight bold
  font-size 2em
  &:not(:last-child)::after
    content ','

@media (max-width 1000px)
  main
    grid-template-columns 1fr
  section.right
    top: 0
</style>
