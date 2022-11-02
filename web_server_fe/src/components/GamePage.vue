<script lang="ts">
import { useGameStore } from "@/stores/game";
import { io } from "socket.io-client";
import { defineComponent } from "vue";

export default defineComponent({
  components: {},
  props: {
    uuid: String,
  },
  data() {
    return {
        store: useGameStore(),
        socket: io(),
    };
  },
  methods: {},
});
</script>

<template>Lets game!</template>
