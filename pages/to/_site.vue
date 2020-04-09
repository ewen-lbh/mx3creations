<template lang="pug">
main
  template(v-if="Object.keys(sites).includes(site)")
    p
      | Redirection vers {{ $t(site) }} (
      a(:href="sites[site]") {{ sites[site] }}
      | )...
  template(v-else)
    p Hm. Impossible de vous rediriger vers {{ $t(site) }}.
    BtnOutline(href="/" style="display:flex;justify-content:center") {{ $t('goHome') }}
</template>

<script>
import BtnOutline from '~/components/BtnOutline.vue'
const sites = require('static/sites.json')

export default {
  components: { BtnOutline },
  fetch({ route, redirect }) {
    const site = route.params.site
    if (Object.keys(sites).includes(site)) {
      redirect(301, sites[site])
    } else {
      // redirect('/')
    }
  },
  data() {
    return { sites, site: this.$route.params.site }
  },
  mounted() {
    // Client-side redirect as a fallback
    if (Object.keys(this.sites).includes(this.site)) {
      window.location = this.sites[this.site]
    }
  },
  beforeDestroy() {
    window.clearInterval(this.animatedDotsInterval)
  }
}
</script>
