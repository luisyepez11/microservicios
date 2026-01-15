<script setup>
import { ref, onMounted } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const router = useRoute(); // Para redirigir si es necesario
const productos = ref([])
const mensaje = ref('')

// Modelo del formulario
const lote = ref({
  id_producto: router.params.id,
  cantidad: 0,
  nombreProduco:"",
  stockActual:0,
  fecha_llegada: new Date().toISOString().split('T')[0] // Fecha actual por defecto formato YYYY-MM-DD
})

const tokenGuardado = localStorage.getItem('authToken');


const cargar = async () => {
    const productoData = await axios.get(`http://localhost:8000/api/products/${router.params.id}`)
    const stockData = await axios.get(`http://localhost:8003/api/${router.params.id}`)
    lote.value.nombreProduco=productoData.data.name
    lote.value.stockActual = stockData.data.cantidad
}

// 2. Enviar el formulario
const registrarLote = async () => {
  if(!lote.value.id_producto || lote.value.cantidad <= 0) {
    alert("Por favor selecciona un producto y una cantidad válida.")
    return
  }

  try {
    await axios.put("http://localhost:8003/api/actualizarProductos", [{
        id_producto:Number(router.params.id),
        cantidad:lote.value.cantidad+lote.value.stockActual
    }])
    
    alert("Lote registrado exitosamente")
    lote.value.cantidad = 0
    lote.value.id_producto = ""
    
  } catch (error) {
    console.error("Error registrando lote:", error)
    alert("Hubo un error al registrar el lote")
  }
}

onMounted(() => {
  cargar()
})
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <sideBar></sideBar>

    <div class="flex-1 ml-40">
      <NavBar></NavBar>

      <main class="max-w-4xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
        
        <div class="bg-slate-800/80 border border-slate-700 rounded-lg shadow-xl overflow-hidden">
          
          <div class="bg-slate-900/80 border-b border-slate-700 px-6 py-4">
            <h2 class="text-lg font-semibold text-emerald-400 uppercase tracking-wide">
              Registrar Llegada de Lote
            </h2>
            <p class="text-slate-400 text-sm mt-1">Ingresa los detalles del nuevo ingreso de mercancía.</p>
          </div>

          <div class="p-8">
            <form @submit.prevent="registrarLote" class="space-y-6">
              
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">
                  Producto
                </label>
                <label class="block text-2xl font-medium text-slate-300 mb-2">
                  {{ lote.nombreProduco }}
                </label>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-slate-300 mb-2">
                    Cantidad de Entrada
                  </label>
                  <input 
                    type="number" 
                    v-model="lote.cantidad"
                    min="1"
                    class="w-full bg-slate-900 border border-slate-600 text-slate-100 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block p-2.5"
                    placeholder="Ej: 50"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-slate-300 mb-2">
                    Fecha de Llegada
                  </label>
                  <input 
                    type="date" 
                    v-model="lote.fecha_llegada"
                    class="w-full bg-slate-900 border border-slate-600 text-slate-100 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block p-2.5 [color-scheme:dark]"
                  />
                </div>
              </div>

              <div class="flex justify-end pt-4">
                <button
                  type="submit"
                  class="px-6 py-2.5 rounded-lg font-bold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition duration-150 shadow-lg hover:shadow-emerald-500/20"
                >
                  Registrar Entrada
                </button>
              </div>

            </form>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>