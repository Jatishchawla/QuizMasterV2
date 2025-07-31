<script setup>

import NavPage from './components/NavPage.vue'
import FootPage from'./components/FootPage.vue'

</script>

<template>
  <!-- <Base/> -->
  <!-- <NavPage/> -->

  <!-- Main Content Slot -->
  <div style="min-height: 90vh;">
    <RouterView/>
  </div>
  <!-- <FootPage/> -->
</template>

<style scoped>
</style>
