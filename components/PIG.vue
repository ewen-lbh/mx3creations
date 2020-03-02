<template lang="pug">
#pig
</template>

<script>
import path from 'path'

export default {
  props: {
    images: {
      type: Array
    }
  },
  data() {
    // eslint-disable-next-line no-unused-vars
    const app = this
    return {
      options: {
        urlForSize: (filename, size) => {
          filename = filename.replace(/^https?:\/\/static.mx3creations.com/, '')
          return (
            'http://static.mx3creations.com' +
            path.join(
              path.dirname(filename),
              'thumbs',
              size.toString(),
              path.basename(filename)
            )
          )
        },
        onClickHandler(filename) {
          app.$emit('image-click', filename.replace(/\/thumbs\/\d+/, ''))
        },
        getMinAspectRatio(lastWindowWidth) {
          // Phones
          if (lastWindowWidth <= 640) return 1
          // Tablets
          else if (lastWindowWidth <= 1280) return 2
          // Laptops
          else if (lastWindowWidth <= 1920) return 3.5
          // Large desktops
          return 4
        },
        getImageSize(lastWindowWidth) {
          if (lastWindowWidth <= 700)
            // Phones
            return 250
          return 500
        },
        spaceBetweenImages: 20
      }
    }
  },
  mounted() {
    window.pig = new window.Pig(this.images, this.options).enable()
  }
}
</script>

<style lang="stylus">
#pig
  height: 100vh

.pig-figure img
  background: white

.pig-figure
  cursor: pointer
</style>
