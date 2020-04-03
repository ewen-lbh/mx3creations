<template lang="pug">
main
  template(v-if="$route.params.status == 'sent'")
    h1 Merci !
    p.ill-answer-asap Je vous répondrais le plus vite possible
  template(v-else)
    h1 Me contacter
  section: form(name="contact" data-netlify="true" method="POST" action="/contact/sent")
    p: label 
      | Votre e-mail
      input(type="email" name="email")
    p: label
      | Votre message
      textarea(rows="20" cols="40" name="message")
    
    p: BtnOutline(type="submit") Envoyer
</template>

<script>
import BtnOutline from '~/components/BtnOutline.vue'

export default {
  components: { BtnOutline }
}
</script>

<style lang="stylus" scoped>
form
  display flex
  justify-content center
  flex-direction column
  align-items center
  width 100%
  label, p
    display flex
    align-items center
    flex-direction column
    text-align center
  p, label, input, textarea
    width 100%

.ill-answer-asap
  text-align center
</style>
