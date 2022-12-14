import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/lobby/:type",
      name: "lobby",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/LobbyView.vue"),
    },
    {
      path: "/game/:uuid",
      name: "game",
      component: () => import("../views/GameView.vue"),
    },
    {
      path: "/showoff/:uuid",
      name: "showoff",
      component: () => import("../views/ShowoffView.vue"),
    },
  ],
});

export default router;
