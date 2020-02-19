<template lang="pug">
NavItem.--nav-language-switch
  nuxt-link(
    :to="switchLocalePath('en')"
    :class="{ current: $i18n.locale === 'en' }"
    title="English"
  ) EN
  span.sep /
  nuxt-link(
    :to="switchLocalePath('fr')"
    :class="{ current: $i18n.locale === 'fr' }"
    title="Français"
  ) FR
</template>

<script>
import NavItem from '~/components/NavItem.vue'

export default {
  components: { NavItem }
}
</script>

<style lang="stylus" scoped>
.sep
  opacity .25
.current
  opacity: 0.5
</style>
