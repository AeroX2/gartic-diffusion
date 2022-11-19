import { defineStore } from "pinia";
import { io, Socket } from "socket.io-client";

const events: string[] = [
  "connect",
  "game_start",
  "game_finish",
  "game_next_state",

  "lobby_update",
];

export const useSocketStore = () => {
  const innerStore = defineStore("socketio", {
    state: () => ({
      socket: undefined as Socket | undefined,
      callbacks: new Map(),
    }),
    actions: {
      init() {
          this.socket = io();
          for (const event of events) {
            this.socket.on(event, (data: any) => {
              debugger;
              this.callbacks.get(event)?.(data);
            });
          }
      },
      on(event: string, callback: (data: any) => void) {
        if (events.indexOf(event) === -1) {
          console.error(`Event ${event} is missing from events`)
          return
        }
        this.callbacks.set(event, callback);
      },
      emit(event: string, ...args: any[]) {
        this.socket?.emit(event, ...args);
      },
    },
  });
  const s = innerStore();
  s.init();
  return s;
}
