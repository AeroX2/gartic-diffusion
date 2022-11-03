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
      socket: io("http://localhost:5000"),
    };
  },
  mounted() {},
});
</script>

<template></template>
