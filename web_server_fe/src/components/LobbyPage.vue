<script lang="ts">
import { defineComponent } from "vue";
import { io, Socket } from "socket.io-client";
import { v4 as uuid } from "uuid";
import UserDialog from "./UserDialog.vue";
import JoinLobbyDialog from "./JoinLobbyDialog.vue";
import { useLobbyStore } from "../stores/lobby";

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
      socket: io("http://localhost:5000"),
    };
  },
  mounted() {
    if (this.$props.type === "create") {
      this.store.creating();
    } else if (this.$props.type === "join") {
      this.store.joining();
    } else {
      console.error("Invalid type for LobbyPage");
    }
  },
  methods: {
    joinLobby(code: string) {
      this.store.submitJoin(code);
    },
    setUsername(username: string) {
      this.store.submitUsername(username, this.connectToLobby);
    },
    connectToLobby() {
      this.socket.on("lobby_update", (data) => {
        if (data.error) {
          // TODO handle error
          return;
        }
        this.store.lobby = data.lobby;
      });

      if (this.$props.type === "create") {
        this.socket.on("lobby_create_response", (data) => {
          if (data.error) {
            // TODO handle error
            return;
          }
          this.store.lobby = data.lobby;
          this.store.code = data.code;
          this.store.doneLoading();
        });
        this.socket.emit("lobby_create", { username: this.store.username });
      } else if (this.$props.type === "join") {
        this.socket.on("lobby_join_response", (data) => {
          if (data.error) {
            // TODO handle error
            return;
          }
          this.store.lobby = data.lobby;
          this.store.doneLoading();
        });
        this.socket.emit("lobby_join", {
          code: this.store.code,
          username: this.store.username,
        });
      }
    },
    kickUser() {},
  },
});
</script>

<template>
  <JoinLobbyDialog
    v-bind:show-dialog="store.state === 'joining'"
    v-on:confirm="joinLobby"
  />
  <UserDialog
    v-bind:show-dialog="store.state === 'username'"
    v-on:confirm="setUsername"
  />
  <div v-if="store.state === 'loading'">
    <ProgressSpinner />
  </div>
  <div v-if="store.state === 'done'">
    <h4>Users</h4>
    <div class="grid">
      <div class="col-4" v-for="user in store.lobby?.users">
        <Card>
          <template #content>
            {{ user.name }}
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>
