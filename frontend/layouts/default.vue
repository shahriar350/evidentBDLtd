<template>
  <v-app>
    <v-app-bar
      fixed
      app
    >
      <!--      <v-toolbar-title v-text="title"/>-->
      <v-toolbar-title>
        <nuxt-link to="/">Homepage</nuxt-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn to="/auth/login" color="primary">Login</v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt/>
      </v-container>
    </v-main>
    <v-footer :absolute="true"
              app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  components: {

  },
  data() {
    return {
      title: 'Admin panel'
    }
  }
}
</script>
