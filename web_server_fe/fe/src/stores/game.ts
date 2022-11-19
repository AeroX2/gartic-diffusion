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
      imageUrl: undefined as string | undefined,
      description: "",
      roundSeconds: 20,
      roundTimerStart: 0,
      roundTimerCurrent: 0,
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
