<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
const usuario = ref('Usuario')
const fechaActual = ref(new Date().toLocaleDateString())

const cerrarSesion = () => {
    localStorage.removeItem('authToken');
}
const tokenGuardado = localStorage.getItem('authToken');
const cargar = async () =>{
try {
    const response =await axios.get("http://127.0.0.1:8001/mi-perfil", {
    headers: {
        'Authorization': `Bearer ${tokenGuardado}`
    }
})
    console.log(response.data)
} catch (error) {
    console.log(error)
}
}
cargar()
</script>

<template>
<div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <sideBar></sideBar>
    <!-- Main Content -->
    <div class="flex-1 ml-40">
        <!-- Navbar -->
        
        <NavBar></NavBar>
        <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div class="px-4 py-6 sm:px-0">
                
            </div>
        </main>
    </div>
</div>
</template>

<style>

</style>