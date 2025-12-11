<script setup>
import { ref } from 'vue'
import axios from 'axios';
const permisos = ref([])
const tokenGuardado = localStorage.getItem('authToken');
const cargar = async () =>{
  try {
    const response =await axios.get("http://127.0.0.1:8001/mi-perfil", {
    headers: {
        'Authorization': `Bearer ${tokenGuardado}`
    }
    
})
permisos.value = response.data.permisos
console.log(permisos.value)
  } catch (error) {
    console.log(error)
  }
}
cargar()
const tienePermiso = (nombrePermiso) => {
  return permisos.value.some(permiso => permiso.nombre_permiso === nombrePermiso);
};
</script>
<template>
  <nav
    class="bg-slate-900 text-slate-100 w-40 flex flex-col items-center py-8 fixed top-0 bottom-0 left-0 z-10 shadow-lg border-r border-slate-800"
  >
    <div class="font-bold text-2xl mb-12 text-slate-100"></div>

    <ul class="flex flex-col items-center w-full gap-2">
      <li
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/home"
        >
          Principal
        </a>
      </li>
      <li 
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/product"
        >
          Productos
        </a>
      </li>
      <li v-if="tienePermiso('vista_stock')"
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/stock"
        >
          Almacen
        </a>
      </li>
      <li v-if="tienePermiso('manejo_usuarios')"
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/user"
        >
          Usuarios
        </a>
         <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/user"
        >
        </a>
      </li>
        <li v-if="tienePermiso('modificacion_productos')"
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/gestion_producto"
        >
          Gestion Producto
        </a>
      </li>
    </ul>
  </nav>
</template>