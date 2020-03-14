<template lang="pug">
.--work
  h1 {{ name }}
  .description(v-html="description")
  img(v-if="front" :src="`/works/${directory}/${front}`")
</template>

<script>
export default {
  props: {
    description: String,
    name: String,
    front: String,
    directory: String
  }
}
</script>
