import { defineStore } from "pinia";

export const useGameStore = defineStore("game", {
  state: () => {
    return {
      state: "initial",
    };
  },
  actions: {
    initialDescribed() {
      this.state = 'loading';
    },
    loaded() {
      this.state = 'describe';
    },
    described() {
      this.state = 'loading';
    },
    done() {
      this.state = 'done';
    }
  },
});
