<script lang="ts">
import { io } from "socket.io-client";
import { defineComponent } from "vue";

export default defineComponent({
  components: {},
  props: {
    uuid: String,
  },
  data() {
    return {
      socket: io(),
    };
  },
  mounted() {},
});
</script>

<template></template>
