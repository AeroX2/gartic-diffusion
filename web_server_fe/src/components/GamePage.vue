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
  mounted() {
    this.socket.on("game_next_state", ({ state, imageUrl }) => {
      this.store.imageUrl = imageUrl;
      this.store.state = state;
    });

    this.socket.on("game_finish", () => {
      this.$router.push(`/showoff/${this.$props.uuid}`);
    });
  },
});
</script>

<template>
  <Card>
    <img
      class="w-full border-round-sm"
      v-if="store.imageUrl"
      v-bind:src="store.imageUrl"
    />
    {{
      store.state === "initial"
        ? "Describe a scene you want to have generated"
        : "Describe the scene above"
    }}
    <span class="p-float-label">
      <InputText
        id="description"
        class="w-full"
        autocomplete="off"
        v-model="store.description"
        autofocus
      />
      <label for="description">Description</label>
    </span>
  </Card>
</template>
