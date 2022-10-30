import { defineStore } from "pinia";

type User = {
  name: string;
  uuid: string;
};

export const useLobbyStore = defineStore("lobby", {
  state: () => {
    return { state: "initial", code: "", username: "", users: [] as User[] };
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
    submitUsername(username: string) {
      this.username = username;
      this.state = "loading";
    },
    doneLoading() {
      this.state = "done";
    },
  },
});
