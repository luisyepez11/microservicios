<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
const usuarios = ref([
  {
    id_usuario: 1,
    correo_usuario: 'juan@example.com',
    fecha_creacion: '2025-12-01T10:00:00'
  },
  {
    id_usuario: 2,
    correo_usuario: 'maria@example.com',
    fecha_creacion: '2025-12-02T15:30:00'
  }
])
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
    const listaUsuarios = await axios.get("http://127.0.0.1:8001/usuarios")
    usuarios.value = listaUsuarios.data;
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
        <table
          class="min-w-full border border-slate-700 rounded-lg overflow-hidden shadow-xl bg-slate-800/80"
        >
          <thead class="bg-slate-900/80 border-b border-slate-700">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider"
              >
                Correo
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider"
              >
                Fecha de creación
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider"
              >
                Acción
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr
              class="bg-slate-900/70 hover:bg-slate-800 transition duration-150"
              v-for="usuario in usuarios"
              :key="usuario.id_usuario"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                {{ usuario.correo_usuario }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                {{ (usuario.fecha_creacion.split('T'))[0] }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                <router-link
                  :to="{ name: 'user-detail', params: { id: usuario.id_usuario } }"
                >
                  <button
                    class="bg-emerald-500 text-slate-950 px-4 py-2 rounded-lg hover:bg-emerald-400 active:scale-[0.98] transition duration-150 font-semibold shadow-sm hover:shadow-md"
                  >
                    Ver
                  </button>
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </main>
    </div>
  </div>
</template>