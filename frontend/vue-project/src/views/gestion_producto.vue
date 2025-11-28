<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import Card from '@/components/card.vue';
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
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <!-- Sidebar -->
    <sideBar></sideBar>

    <!-- Main Content -->
    <div class="flex-1 ml-40">
      <!-- Navbar -->
      <NavBar></NavBar>

      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="grid px-4 py-6 sm:px-0 grid-cols-4 gap-6">
          <Card textoBoton="modificar"></Card>
        </div>
      </main>
    </div>
  </div>
</template>