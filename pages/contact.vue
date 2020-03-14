<template lang="pug">
main
  h1 Me contacter
  section: form(name="contact" netlify)
    p: label 
      | Votre e-mail
      input(type="email" name="email")
    p: label
      | Votre message
      textarea(rows="20" cols="40")
    
    p: button(type="submit") Envoyer
</template>

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
</style>
