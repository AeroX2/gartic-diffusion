<script setup lang="ts">
import GamePage from "../components/GamePage.vue";
</script>

<template>
  <main>
    <GamePage v-bind:uuid="$route.params.uuid as string" />
  </main>
</template>
