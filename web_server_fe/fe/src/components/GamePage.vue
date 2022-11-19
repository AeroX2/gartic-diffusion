<script lang="ts">
import { useGameStore } from "@/stores/game";
import { useSocketStore } from "@/stores/socketio";
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
      socket: useSocketStore(),
    };
  },
  mounted() {
    this.socket.on(
      "game_next_state",
      ({ state, imageUrl }: { state: string; imageUrl: string }) => {
        console.log("Game state changed", state, imageUrl);
        this.store.state = state;
        if (state === "loading") {
          this.socket.emit("game_response", {
            description: this.store.description,
          });
        } else {
          this.store.imageUrl = imageUrl;
          this.store.roundTimerStart = new Date().getTime();
        }
      }
    );

    this.socket.on("game_finish", () => {
      this.$router.push(`/showoff/${this.$props.uuid}`);
    });

    this.store.roundTimerStart = new Date().getTime();
    this.store.roundTimerCurrent = new Date().getTime();
    setInterval(() => {
      this.store.roundTimerCurrent = new Date().getTime();
    }, 500);
  },
  computed: {
    timeLeftRemaining() {
      return (
        this.store.roundSeconds -
        Math.floor(
          (this.store.roundTimerCurrent - this.store.roundTimerStart) / 1000
        )
      );
    },
  },
});
</script>

<template>
  <Card>
    <template #content>
      <ProgressBar v-if="store.state === 'loading'" mode="indeterminate" />
      <div v-if="store.state !== 'loading'">
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
        <br />
        {{ `Timer: ${timeLeftRemaining} seconds left` }}
        <span class="p-float-label mt-5">
          <InputText
            id="description"
            class="w-full"
            autocomplete="off"
            v-model="store.description"
            autofocus
          />
          <label for="description">Description</label>
        </span>
      </div>
    </template>
  </Card>
</template>
