<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
const usuarios = ref({})
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
<div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <sideBar></sideBar>
    <!-- Main Content -->
    <div class="flex-1 ml-40">
        <!-- Navbar -->
        
        <NavBar></NavBar>
        <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <table class="min-w-full border-2 border-gray-300 rounded-lg overflow-hidden shadow-md">
    <thead class="bg-gray-100 border-b-2 border-gray-300">
        <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Encabezado 1
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Encabezado 2
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Encabezado 3
            </th>
        </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
        <tr class="hover:bg-gray-50 transition duration-150" v-for="usuario in usuarios">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{usuario.correo_usuario}}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{(usuario.fecha_creacion.split("T"))[0]}}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-150 font-medium shadow-sm hover:shadow-md">ver</button>
            </td>
        </tr>
    </tbody>
</table>
        </main>
    </div>
</div>
</template>

<style>

</style>