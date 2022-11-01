<script lang="ts">
import { defineComponent } from "vue";
import { io } from "socket.io-client";
import UserDialog from "./UserDialog.vue";
import JoinLobbyDialog from "./JoinLobbyDialog.vue";
import { useLobbyStore } from "../stores/lobby";
import { toSvg } from "jdenticon";
import QRCode from "qrcode";

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
      socket: io("http://localhost:5000"),
      qrcodeUrl: "",
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

      if (this.$props.type === "create") {
        this.socket.on("lobby_create_response", (data) => {
          if (this.handleError(data)) return;

          this.store.lobby = data.lobby;
          this.store.code = data.code;
          this.store.doneLoading();
          this.generateQr();
        });
        this.socket.emit("lobby_create", { username: this.store.username });
      } else if (this.$props.type === "join") {
        this.socket.on("lobby_join_response", (data) => {
          if (this.handleError(data)) return;

          this.store.lobby = data.lobby;
          this.store.doneLoading();
          this.generateQr();
        });
        this.socket.emit("lobby_join", {
          code: this.store.code,
          username: this.store.username,
        });
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
    identicon(username: string) {
      return toSvg(username, 50);
    },
    generateQr() {
      QRCode.toDataURL(this.store.code, { errorCorrectionLevel: "H" }).then(
        (url: string) => {
          this.qrcodeUrl = url;
        }
      );
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
      <div class="flex">
        <div class="flex flex-column">
          Code: {{ store.code }}
          <img class="border-round-sm" v-bind:src="qrcodeUrl" />
        </div></div
    ></template>
    <div v-if="store.state !== 'done'">
      <ProgressSpinner />
    </div>
    <div class="flex flex-column gap-2">
      Users
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
