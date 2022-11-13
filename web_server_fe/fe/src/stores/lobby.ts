import { defineStore } from "pinia";

type User = {
  name: string;
  uuid: string;
};

type Lobby = {
  uuid: string;
  users: User[];
};

export const useLobbyStore = defineStore("lobby", {
  state: () => {
    return {
      state: "initial",
      code: "",
      username: "",
      lobby: null as Lobby | null,
    };
  },
  actions: {
    creating() {
      this.state = "username";
    },
    joining() {
      this.state = "joining";
    },
    submitJoin(code: string) {
      this.code = code;
      this.state = "username";
    },
    submitUsername(username: string, callback: () => void) {
      this.username = username;
      this.state = "loading";
      callback();
    },
    doneLoading() {
      this.state = "done";
    },
  },
});
