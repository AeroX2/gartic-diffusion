<script lang="ts">
import { defineComponent } from "vue";
import UserDialog from "./UserDialog.vue";
import JoinLobbyDialog from "./JoinLobbyDialog.vue";
import { useLobbyStore } from "../stores/lobby";
import { toSvg } from "jdenticon";
import { useSocketStore } from "@/stores/socketio";

export default defineComponent({
  components: {
    UserDialog,
    JoinLobbyDialog,
  },
  props: {
    type: String,
  },
  data() {
    return {
      store: useLobbyStore(),
      error: undefined as string | undefined,
      socket: useSocketStore(),
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      if (this.$props.type === "create") {
        this.store.creating();
      } else if (this.$props.type === "join") {
        this.store.joining();
      } else {
        console.error("Invalid type for LobbyPage");
      }
    },
    joinLobby(code: string) {
      this.error = undefined;
      this.store.submitJoin(code);
    },
    setUsername(username: string) {
      this.error = undefined;
      this.store.submitUsername(username, this.connectToLobby);
    },
    connectToLobby() {
      this.socket.on("lobby_update", (data) => {
        if (this.handleError(data)) return;

        this.store.lobby = data.lobby;
      });

      this.socket.on("game_start", () => {
        this.$router.push(`/game/${this.store.lobby?.uuid}`);
      });

      if (this.$props.type === "create") {
        this.socket.emit(
          "lobby_create",
          { username: this.store.username },
          (data: any) => {
            if (this.handleError(data)) return;

            this.store.lobby = data.lobby;
            this.store.code = data.code;
            this.store.doneLoading();
          }
        );
      } else if (this.$props.type === "join") {
        this.socket.emit(
          "lobby_join",
          {
            code: this.store.code,
            username: this.store.username,
          },
          (data: any) => {
            if (this.handleError(data)) return;

            this.store.lobby = data.lobby;
            this.store.doneLoading();
          }
        );
      }
    },
    handleError(data: { error: string }) {
      if (data.error) {
        this.error = data.error;
        this.init();
        return true;
      }
      this.error = undefined;
      return false;
    },
    startGame() {
      this.socket.emit("lobby_start_game", { uuid: this.store.lobby?.uuid });
      this.$router.push(`/game/${this.store.lobby?.uuid}`);
    },
    identicon(username: string) {
      return toSvg(username, 50);
    },
  },
});
</script>

<template>
  <JoinLobbyDialog
    v-bind:show-dialog="store.state === 'joining'"
    v-bind:error="error"
    v-on:confirm="joinLobby"
  />
  <UserDialog
    v-bind:show-dialog="store.state === 'username'"
    v-bind:error="error"
    v-on:confirm="setUsername"
  />
  <Panel>
    <template #header>
      <div class="flex justify-content-between w-full">
        <div class="flex flex-column text-5xl">Code: {{ store.code }}</div>
        <Button
          @click="startGame()"
          class="p-button-success"
          icon="pi pi-check"
          iconPos="right"
          label="Start"
        />
      </div>
    </template>
    <div class="flex flex-column gap-2">
      Users
      <div v-if="store.state !== 'done'">
        <ProgressSpinner />
      </div>
      <div class="grid">
        <div class="col-4" v-for="user in store.lobby?.users">
          <div class="surface-50 shadow-4 border-round-sm">
            <div class="flex align-items-center gap-2">
              <div
                class="flex align-items-center"
                v-html="identicon(user.name)"
              ></div>
              {{ user.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </Panel>
</template>
