<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
import Productos from './productos.vue';

const usuario = ref('Usuario')
const fechaActual = ref(new Date().toLocaleDateString())
// Inicializamos datos como null para verificar si cargó
const datos = ref(null) 
const tokenGuardado = localStorage.getItem('authToken');
const datosPermisos = ref([])

// Variables para los contadores de las tarjetas
const cantidadPedidos = ref(0)
const cantidadCompras = ref(0)
const cantidadProductos = ref(0)
const cantidadUsuarios = ref(0)
const topProductos = ref([])

const cargar = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8001/mi-perfil", {
      headers: {
        'Authorization': `Bearer ${tokenGuardado}`
      }
    })
    const pedidos = await axios.get(`http://localhost:8080`)
    const pagos = await axios.get(`http://localhost:3000/api/pagos`)
    const  producto = await axios.get(`http://localhost:8000/api/products`)
    const catidadesProductosPedidos = await axios.get(`http://localhost:8080/cantidadPeidosProductos`)
    datos.value = response.data
    datosPermisos.value = datos.value.permisos
    
    cantidadPedidos.value = pedidos.data.length 
    cantidadCompras.value = pagos.data.length 
    cantidadProductos.value = producto.data.length
    topProductos.value  = producto.data.map(p=>{
      p.cantidadPedidos=catidadesProductosPedidos.data.find(pp=>p.product_id==pp[0])[1]
      return p 
    })
    topProductos.value = topProductos.value.sort((a,b)=> b.cantidadPedidos-a.cantidadPedidos).slice(0,3)
  } catch (error) {
    console.log(error)
  }
}
cargar()
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <sideBar :permisos="datosPermisos"></sideBar>

    <div class="flex-1 ml-40">
      <NavBar></NavBar>

      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        
        <div class="px-4 mb-6" v-if="datos">
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

        <div class="px-4 grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-lg flex items-center justify-between hover:border-emerald-500/50 transition duration-300 group">
            <div>
              <p class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-1">
                Pedidos Realizados
              </p>
              <p class="text-3xl font-bold text-slate-100 group-hover:text-emerald-400 transition-colors">
                {{ cantidadPedidos }}
              </p>
            </div>
            <div class="h-12 w-12 rounded-full bg-slate-700/50 flex items-center justify-center text-2xl group-hover:bg-emerald-500/20 group-hover:text-emerald-400 transition-all">
              📦
            </div>
          </div>

          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-lg flex items-center justify-between hover:border-emerald-500/50 transition duration-300 group">
            <div>
              <p class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-1">
                Compras Realizadas
              </p>
              <p class="text-3xl font-bold text-slate-100 group-hover:text-emerald-400 transition-colors">
                {{ cantidadCompras }}
              </p>
            </div>
            <div class="h-12 w-12 rounded-full bg-slate-700/50 flex items-center justify-center text-2xl group-hover:bg-emerald-500/20 group-hover:text-emerald-400 transition-all">
              💳
            </div>
            
          </div>
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-lg flex items-center justify-between hover:border-emerald-500/50 transition duration-300 group">
            <div>
              <p class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-1">
                Productos Registrados
              </p>
              <p class="text-3xl font-bold text-slate-100 group-hover:text-emerald-400 transition-colors">
                {{ cantidadProductos }}
              </p>
            </div>
            <div class="h-12 w-12 rounded-full bg-slate-700/50 flex items-center justify-center text-2xl group-hover:bg-emerald-500/20 group-hover:text-emerald-400 transition-all">
              🛍️
            </div>
            
          </div>
          <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-lg flex flex-col justify-between hover:border-emerald-500/50 transition duration-300">
            <div class="flex items-center justify-between mb-4">
               <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">🔥 Top 3 Más Pedidos</p>
               <span class="text-xl">🏆</span>
            </div>
            
            <div class="space-y-3">
              <div v-for="(prod, index) in topProductos" :key="index" class="flex items-center justify-between">
                <div class="flex items-center">
                  <span 
                    class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold mr-3"
                    :class="{
                      'bg-yellow-500 text-slate-900': index === 0,
                      'bg-slate-400 text-slate-900': index === 1,
                      'bg-orange-700 text-slate-100': index === 2
                    }"
                  >
                    {{ index + 1 }}
                  </span>
                  <span class="text-slate-200 font-medium text-sm">{{ prod.name }}</span>
                </div>
                <span class="text-emerald-400 font-bold text-sm">{{ prod.cantidadPedidos }} pedidos</span>
              </div>
              
              <div v-if="topProductos.length === 0" class="text-xs text-slate-500 text-center py-2">
                No hay suficientes datos
              </div>
            </div>
          </div>

        </div>

      </main>
    </div>
  </div>
</template>