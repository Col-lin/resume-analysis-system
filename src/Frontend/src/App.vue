<template>
    <div class="app-container" v-if="!infoStore.is_mobile">
        <navBar />
        <div class="content-container">
            <router-view />
        </div>
    </div>
    <div v-else>
        <MobileView />
    </div>
</template>

<script setup>
import navBar from '@/components/common/navBar.vue'

const infoStore = InfoStore()
</script>

<style>
.app-container {
    position: relative;
}

.content-container {
    margin-top: 5%;
}

html {
    font-size: 10px;
}

body {
    background-image: url(./assets/bc.jpg);
    background-size: cover;
    background-attachment: fixed;
}
</style>
