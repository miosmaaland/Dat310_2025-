<template>
  <main id="app" class="min-vh-100 d-flex flex-column">
    <router-view />
  </main>
</template>

<script>
export default {
  methods: {
    logout() {
      fetch('/api/logout', { method: 'POST' })
        .then(() => {
          localStorage.clear();
          this.$router.push('/login');
        });
    },
  },
};
</script>

<style>
html, body, #app {
  height: 100%;
}
</style>