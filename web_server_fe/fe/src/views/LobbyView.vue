<script setup lang="ts">
import LobbyPage from "../components/LobbyPage.vue";
</script>

<template>
  <main>
    <LobbyPage v-bind:type="$route.params.type as string" />
  </main>
</template>
