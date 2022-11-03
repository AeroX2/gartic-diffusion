import { defineStore } from "pinia";

const stateTree = {
  initial: "loading",
  loading: "describe",
  describe: "loading",
};

export const useGameStore = defineStore("game", {
  state: () => {
    return {
      state: "initial",
      imageUrl: undefined,
      rounds: 10,
      description: "",
    };
  },
  actions: {
    initialDescribed() {
      this.state = "loading";
    },
    loaded() {
      this.state = "describe";
    },
    described() {
      this.state = "loading";
    },
    done() {
      this.state = "done";
    },
  },
});
