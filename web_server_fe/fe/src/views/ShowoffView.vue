<script setup lang="ts">
import ShowoffPage from "../components/ShowoffPage.vue";
</script>

<template>
  <main>
    <ShowoffPage v-bind:uuid="$route.params.uuid as string" />
  </main>
</template>
