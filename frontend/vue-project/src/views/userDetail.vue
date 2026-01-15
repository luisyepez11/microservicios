<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios'
import { useRoute } from 'vue-router';
const permisosAgregar = ref([])
const permisosOriginales = ref([])
const permisoQuitar = ref([])
const route = useRoute();
const datos = ref()
const tokenGuardado = localStorage.getItem('authToken');
const cargar = async () =>{
try {
    const datosUsuarios =await axios.get(`http://127.0.0.1:8001/usuarios/${route.params.id}`)
    const datosPermiso = await axios.get(`http://127.0.0.1:8001/permisos`)
    const datosPermisosUsario = await axios.get(`http://127.0.0.1:8001/usuarios/${route.params.id}/permisos`)
    datos.value= datosUsuarios.data
    permisosDisponibles.value = datosPermiso.data
    permisosAsignados.value = datosPermisosUsario.data.permisos
    permisosOriginales.value = datosPermisosUsario.data.permisos.map(p=>p)
    usuario.value={
      nombre: 'Nombre del usuario',
      correo: datos.value.correo_usuario,
      ultimaSesion: `Último inicio de sesión: ${(datos.value.ultima_conexion).split('T')[0]}`,
    }
    console.log(permisosAsignados.value)
} catch (error) {
    console.log(error)
}
}

//esto es para probar jiji
const usuario = ref({
  nombre: 'Nombre del usuario',
  correo: 'correo@ejemplo.com',
  ultimaSesion: 'Último inicio de sesión: --/--/---- --:--',
})
const permisosAsignados = ref([
  {nombre_permiso:'Vista de productos',id_permiso:""},
  {nombre_permiso:'Gestión de inventario',id_permiso:""},
  ]
)

const permisosDisponibles = ref([
  {id_permiso:"",nombre_permiso:'Vista de reportes'},
  {id_permiso:"",nombre_permiso:'Vista de reportes'},
  {id_permiso:"",nombre_permiso:'Vista de reportes'},
])
cargar()
const permisoSeleccionado = ref('')

const agregarPermiso = () => {
  permisosAgregar.value.push(permisoSeleccionado.value)
  permisosAsignados.value.push(permisosDisponibles.value.find(p=> p.id_permiso===permisoSeleccionado.value))
  permisosDisponibles.value = permisosDisponibles.value.filter(p=>p.id_permiso!==permisoSeleccionado.value)
  permisoQuitar.value = (permisoQuitar.value.filter(p=>p!==permisoSeleccionado.value))
  
}

const quitarPermiso = (permiso) => {
  permisoQuitar.value.push(permiso)
  permisosDisponibles.value.push(permisosAsignados.value.find(p=>p.id_permiso===permiso))
  permisosAsignados.value = permisosAsignados.value.filter(p=>p.id_permiso!==permiso)
  permisosAgregar.value = (permisosAgregar.value.filter(p=>p!==permiso))

  
}

const guardarCambios = () => {
try {
  

  permisosAsignados.value.map(async p=>{
   if(permisosOriginales.value.find(pe=>pe.id_permiso===p.id_permiso)===undefined){ 
    console.log(p)
    await axios.post(`http://localhost:8001/permisos-usuario`,{
  id_usuario: route.params.id,
  id_permiso: p.id_permiso
})}
  })
  permisoQuitar.value.map(async p=>{
    console.log(p)
   if(permisosOriginales.value.find(pe=>pe.id_permiso===p)!==undefined){ 
    console.log({
  id_usuario: route.params.id,
  id_permiso: p
})
    await axios.delete(`http://localhost:8001/permisos-usuario/`,{
      params:{
  id_usuario: route.params.id,
  id_permiso: p
}})}
  })
  console.log("permisos asignados con exito")
  } catch (error) {
  console.log(error)
}
} 
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <!-- Sidebar -->
    <sideBar />

    <!-- Main Content -->
    <div class="flex-1 ml-40">
      <!-- Navbar -->
      <NavBar />

      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Encabezado -->
        <div class="px-4 mb-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-100">
              Detalles del usuario
            </h1>
            <p class="text-sm text-slate-400 mt-1">
              Revisa la información del usuario y gestiona sus permisos.
            </p>
          </div>
        </div>

        <div class="px-4 space-y-6">
          <!-- Card de datos del usuario -->
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-xl">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <p class="text-sm text-slate-400">
                  Usuario seleccionado
                </p>
                <h2 class="text-xl font-semibold text-slate-100">
                  {{ usuario.nombre }}
                </h2>
                <p class="text-sm text-emerald-400 mt-1">
                  {{ usuario.correo }}
                </p>
                <p class="text-xs text-slate-500 mt-2">
                  {{ usuario.ultimaSesion }}
                </p>
              </div>
              <div class="flex flex-col items-end gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/40">
                  Usuario activo
                </span>
              </div>
            </div>
          </div>

          <!-- Card de permisos -->
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-xl space-y-5">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-semibold text-slate-100">
                  Permisos de los que dispone
                </h3>
                <p class="text-sm text-slate-400 mt-1">
                  Agrega o quita permisos para este usuario.
                </p>
              </div>
            </div>

            <!-- Lista de permisos asignados -->
            <div class="space-y-2">
              <p class="text-sm text-slate-400">
                Permisos actuales:
              </p>

              <div
                v-if="permisosAsignados.length > 0"
                class="flex flex-wrap gap-2"
              >
                <span
                  v-for="permiso in permisosAsignados"
                  :key="permiso.id_permiso"
                  class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-600 text-xs text-slate-100"
                >
                  {{ permiso.nombre_permiso }}
                  <button
                    type="button"
                    class="text-slate-400 hover:text-red-400 transition text-xs"
                    @click="quitarPermiso(permiso.id_permiso)"
                    title="Quitar permiso"
                  >
                    ✕
                  </button>
                </span>
              </div>

              <p v-else class="text-sm text-slate-500 italic">
                Este usuario aún no tiene permisos asignados.
              </p>
            </div>

            <!-- Selector para agregar permisos -->
            <div class="border-t border-slate-700 pt-4 mt-2 space-y-3">
              <p class="text-sm text-slate-400">
                Agregar permiso a este usuario:
              </p>

              <div class="flex flex-col sm:flex-row gap-3 sm:items-center">
                <select
                  v-model="permisoSeleccionado"
                  class="w-full sm:w-72 rounded-lg border border-slate-600 bg-slate-900 text-slate-100 text-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                >
                  <option value="" disabled>Selecciona un permiso...</option>
                  <option
                    v-for="permiso in permisosDisponibles"
                    :key="permiso.id_permiso"
                    :value="permiso.id_permiso"
                  >
                    {{ permiso.nombre_permiso }}
                  </option>
                </select>

                <button
                  type="button"
                  class="px-4 py-2 rounded-lg font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition shadow-sm hover:shadow-md"
                  @click="agregarPermiso"
                >
                  Agregar permiso
                </button>
              </div>
            </div>

            <!-- Botón guardar cambios -->
            <div class="pt-4 flex justify-end">
              <button
                type="button"
                class="px-6 py-2 rounded-lg font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition shadow-sm hover:shadow-md"
                @click="guardarCambios"
              >
                Guardar cambios
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>