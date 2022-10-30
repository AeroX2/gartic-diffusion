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
      socket: io(),
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
      this.store.submitUsername(username);
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
    <li v-for="user in store.users">
      <Card>
        <Button @click="kickUser">{{ user.name }}</Button>
      </Card>
    </li>
  </div>
</template>
