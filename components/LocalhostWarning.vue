<template lang="pug">
aside.--localhost-warning
  p T'es en localhost mec, pas sur le site live.
</template>

<script>
export default {
  mounted() {
    if (process.env.NODE_ENV !== 'production') {
      document.querySelectorAll('.--localhost-warning').forEach((el) => {
        el.style.display = 'block'
        el.addEventListener('click', (ev) => {
          el.style.display = 'none'
        })
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.--localhost-warning
  display: none
  position: fixed
  left: 2em
  bottom: 2em
  background: var(--prim)
  color: var(--text)
  border: 2px solid var(--text)
  padding: 1em
  z-index: 1000000000

h2, p
  margin: 0
</style>
