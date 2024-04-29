import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  routes: [
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/auth/Login.vue"),
      meta: {
        layout: "full",
      },
    },
    {
      path: "/home",
      name: "Home",
      component: () => import("@/views/home/Home.vue"),
      meta: {
        layout: "full",
        requiresAuth: true,
      },
    },
    // {
    //   path: "/user",
    //   name: "User",
    //   component: () => import("@/views/user/User.vue"),
    //   meta: {
    //     pageTitle: "User",
    //     requiresAuth: true,
    //     permission: "user_show",
    //   },
    // },
    // {
    //   path: "/role",
    //   name: "Role",
    //   component: () => import("@/views/role/Role.vue"),
    //   meta: {
    //     pageTitle: "Role",
    //     requiresAuth: true,
    //     permission: "role_show",
    //   },
    // },
    {
      path: "*",
      redirect: "/login",
    },
  ],
});

router.afterEach(() => {
  const appLoading = document.getElementById("loading-bg");
  if (appLoading) {
    appLoading.style.display = "none";
  }
});

export default router;
