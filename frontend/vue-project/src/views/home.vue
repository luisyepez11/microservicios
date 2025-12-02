<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
const usuario = ref('Usuario')
const fechaActual = ref(new Date().toLocaleDateString())
const datos = ref()
const tokenGuardado = localStorage.getItem('authToken');
const cargar = async () =>{
try {
    const response =await axios.get("http://127.0.0.1:8001/mi-perfil", {
    headers: {
        'Authorization': `Bearer ${tokenGuardado}`
    }
})
    datos.value= response.data
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
        <div class="px-4 mb-6">
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl px-5 py-4 flex items-center justify-between shadow-lg">
            <div>
              <p class="text-sm text-slate-400">
                Bienvenido de nuevo 👋
              </p>
              <p class="text-xl font-semibold text-slate-100">
                Hola, <span class="text-emerald-400">{{ datos.correo_usuario.split('@')[0] }}</span>
              </p>
              <p class="text-xs text-slate-500 mt-1">
                Hoy es {{ fechaActual }}
              </p>
            </div>
            <div class="hidden sm:block text-3xl">
              🛒
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>