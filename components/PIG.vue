<template lang="pug">
#pig
</template>

<script>
export default {
  props: {
    images: {
      type: Array
    }
  },
  data() {
    return {
      clickedFilename: null,
      options: {
        urlForSize: (filename, size) => filename,
        onClickHandler(filename) {
          this.$emit('image-clicked')
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
        spaceBetweenImages: 20
      }
    }
  },
  mounted() {
    setTimeout(() => {
      window.pig = new window.Pig(this.images, this.options).enable()
      document.querySelectorAll('figure.pig-figure').forEach((e) => {
        e.addEventListener('click', (ev) => {
          this.$emit('image-click', e.querySelector('img').getAttribute('src'))
        })
      })
    }, 1000)
  }
}
</script>

<style lang="stylus">
.pig-figure img
  background white
.pig-figure
  cursor pointer
  background-image url(https://thumbs.gfycat.com/PotableEmbarrassedFrenchbulldog-small.gif) !important
  background-position center
  background-size contain
</style>
