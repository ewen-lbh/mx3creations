<template lang="pug">
main
  h1 Qui suis-je?
  section
    p.intro
      | Je suis depuis toujours intéressé par la création, le numérique et le
      | langage. Cette curiosité m'a conduit à approfondir en autodidacte plusieurs domaines
      | qui m'intéresse
  section
    h2 Artistique
    p
      | dessin à l'école des beaux-arts de Nîmes, ateliers de peinture, de
      | sculpture. Depuis mes 7 ans, je compose de la musique électronique,
      | j'ai suivi des cours de piano et de DJ et participé à une masterclass
      | de production musicale. Pendant mes années de collège, j'ai réalisé de
      | nombreuses affiches et logos en utilisant divers logiciels (3D, motion
      | design, graphisme&mldr;)
  section
    h2 Numérique
    p
      | j'ai appris à programmer dans différents langages informatiques: HTML,
      | Python et JavaScript, ce qui m'a permis de créer
      a(href='https://mx3creations.com') mon site
      |  et, actuellement,
      a(href='https://www.schoolsyst.com/') une application web pour étudiants
      | . J'ai aussi pour projet la création de plusieurs langages de
      |       programmation.
    p
      | Tout mes projets de programmation sont publiquement visibles sur
      a(href='https://github.com/ewen-lbh') mon profil GitHub
      | : tout mes
      |       projets sont dits "Open Source".
  section
    h2 Linguistique
    p
      | l'anglais étant indispensable à la lecture de documentations, j'ai approfondi cette langue (TOEIC Bridge: 176/180), conversé par mail avec un américain pour réaliser un logo. Je suis aussi fasciné depuis l'enfance par l'écriture: le cyrillique (d'où mon choix de LV3, le russe), le grec (cours particuliers) et les hiraganas et katakanas (japonais en autodidacte).
  section
    h2 Scientifique
    p
      | Le langage mathématique m'intéresse tout autant: Il m'arrive d'appréhender des concepts complexes mathématiques en naviguant sur wikipédia anglais ou en regardant des vidéos de chaînes YouTube telles que "3Blue1Brown" ou "Numerphile"
</template>

<style lang="stylus" scoped>
main
  margin-top: 20px

main /deep/
  & h1, & h2
    font-family Work Sans
  & h1
    font-size 10vmin
  & h2
    font-size 5vmin
    margin-top: 0.5em
    margin-bottom: 0
  & p
    margin-top: 0
    text-align justify
</style>
