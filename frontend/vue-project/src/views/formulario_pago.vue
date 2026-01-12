<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios'
import { useRoute } from 'vue-router';
import router from '../../router';
const route = useRoute();
// --- ESTADO DEL FORMULARIO ---
const procesando = ref(false)
const productos = ref([])
const pago = ref({
  monto: null,
  metodo: 'tarjeta', // 'tarjeta', 'pago_movil', 'efectivo'
  // Datos Tarjeta
  titular: '',
  numero_tarjeta: '',
  fecha_exp: '',
  cvv: '',
  // Datos Pago Móvil
  banco_origen: '',
  telefono_origen: '',
  referencia: '',

})

const bancosVenezuela = ['Banco de Venezuela', 'Banesco', 'Mercantil', 'Provincial', 'BNC', 'Bicentenario']

// --- FUNCIONES ---
const cargar = async () =>{
  const productosResult = await axios.get(`http://localhost:8080/pedidosProductos/${route.params.id}`)
  const calculo = productosResult.data.map(async producto =>{
    const productoResul = await axios.get(`http://localhost:8000/api/products/${producto.idProducto}`)
    return producto.cantidadProducto*productoResul.data.price
    
  })
  const precios = await Promise.all(calculo);
  const sumaTotal = precios.reduce((acc, curr) => acc + curr, 0);
  pago.value.monto = sumaTotal
}
cargar()
const procesarPago = async () => {
  // Validaciones simples
  if (!pago.value.monto || pago.value.monto <= 0) {
    alert('Por favor, indica un monto válido.')
    return
  }

  if (pago.value.metodo === 'pago_movil' && !pago.value.referencia) {
    alert('Debes indicar el número de referencia.')
    return
  } 

  procesando.value = true

  try {
    
    // Preparar payload según el método seleccionado
    const payload = {
      monto: pago.value.monto,
      metodo: pago.value.metodo,
      detalles: {}
    }

    if (pago.value.metodo === 'tarjeta') {
      payload.detalles = {
        titular: pago.value.titular,
        tarjeta: pago.value.numero_tarjeta
      }
    } else if (pago.value.metodo === 'pago_movil') {
      payload.detalles = {
        banco: pago.value.banco_origen,
        telefono: pago.value.telefono_origen,
        referencia: pago.value.referencia
      }
    }

    console.log("Enviando pago...", payload)
    const tokenGuardado = localStorage.getItem('authToken')
    const usuario =await axios.get("http://127.0.0.1:8001/mi-perfil", {
    headers: {
        'Authorization': `Bearer ${tokenGuardado}`
    }
})
    const ahora = new Date();
    const fechaParaPostgres = ahora.toISOString().split('T')[0]; 
    const result = await axios.post(`http://localhost:3000/api/pagos`,{
          idPedido:route.params.id
          ,idUsuario:usuario.data.id_usuario
          ,fechaPago:fechaParaPostgres
          ,MontoPagado:pago.value.monto
          ,metodoPago:pago.value.metodo
    })
    const cambioEstado = await axios.put(`http://localhost:8080/pagarPedido/${route.params.id}`)
    const notificacionPago = await axios.post(`http://localhost:8090/api/notificacion/pago`,{
    correo:usuario.data.correo_usuario
    })
    await new Promise(resolve => setTimeout(resolve, 1500))

    alert('Pago registrado exitosamente')
    resetForm()

  } catch (error) {
    console.error(error)
    alert('Error al procesar el pago')
  } finally {
    procesando.value = false
  }
}

const resetForm = () => {
  pago.value = {
    monto: null,
    metodo: 'tarjeta',
    titular: '',
    numero_tarjeta: '',
    fecha_exp: '',
    cvv: '',
    banco_origen: '',
    telefono_origen: '',
    referencia: ''
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <sideBar></sideBar>
    
    <div class="flex-1 ml-40">
      <NavBar></NavBar>
      
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <h1 class="text-2xl font-bold text-slate-100 mb-6">Procesar Pago</h1>
          
          <div class="bg-slate-800/80 shadow-xl rounded-2xl p-6 border border-slate-700">
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
              
              <div class="lg:col-span-1 space-y-6">
                
                <div>
                  <label for="monto" class="block text-sm font-medium text-slate-200 mb-2">
                    Monto a Pagar
                  </label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400 font-bold">$</span>
                    <input 
                      type="number" 
                      id="monto" 
                      v-model="pago.monto"
                      step="0.01"
                      placeholder="0.00"
                      class="w-full rounded-md border border-slate-700 bg-slate-900 text-slate-100 shadow-sm py-3 pl-8 pr-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-lg font-semibold"
                      readonly
                    >
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-slate-200 mb-3">Método de Pago</label>
                  <div class="space-y-3">
                    
                    <div 
                      @click="pago.metodo = 'tarjeta'"
                      :class="`cursor-pointer p-4 rounded-xl border flex items-center gap-3 transition-all ${pago.metodo === 'tarjeta' ? 'bg-slate-700 border-emerald-500 ring-1 ring-emerald-500' : 'bg-slate-900 border-slate-700 hover:bg-slate-800'}`"
                    >
                      <span class="text-2xl">💳</span>
                      <span :class="pago.metodo === 'tarjeta' ? 'text-emerald-400 font-semibold' : 'text-slate-300'">Tarjeta</span>
                    </div>

                    <div 
                      @click="pago.metodo = 'pago_movil'"
                      :class="`cursor-pointer p-4 rounded-xl border flex items-center gap-3 transition-all ${pago.metodo === 'pago_movil' ? 'bg-slate-700 border-emerald-500 ring-1 ring-emerald-500' : 'bg-slate-900 border-slate-700 hover:bg-slate-800'}`"
                    >
                      <span class="text-2xl">📱</span>
                      <span :class="pago.metodo === 'pago_movil' ? 'text-emerald-400 font-semibold' : 'text-slate-300'">Pago Móvil</span>
                    </div>

                    <div 
                      @click="pago.metodo = 'efectivo'"
                      :class="`cursor-pointer p-4 rounded-xl border flex items-center gap-3 transition-all ${pago.metodo === 'efectivo' ? 'bg-slate-700 border-emerald-500 ring-1 ring-emerald-500' : 'bg-slate-900 border-slate-700 hover:bg-slate-800'}`"
                    >
                      <span class="text-2xl">💵</span>
                      <span :class="pago.metodo === 'efectivo' ? 'text-emerald-400 font-semibold' : 'text-slate-300'">Efectivo</span>
                    </div>

                  </div>
                </div>
              </div>

              <div class="lg:col-span-2 bg-slate-900/50 rounded-xl p-6 border border-slate-700/50">
                
                <h3 class="text-lg font-semibold text-white mb-4 border-b border-slate-700 pb-2">
                  Detalles del Pago
                </h3>

                <div v-if="pago.metodo === 'tarjeta'" class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-1">Nombre del Titular</label>
                    <input type="text" v-model="pago.titular" class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-1">Número de Tarjeta</label>
                    <input type="text" v-model="pago.numero_tarjeta" placeholder="0000 0000 0000 0000" class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-slate-400 mb-1">Vencimiento</label>
                      <input type="text" v-model="pago.fecha_exp" placeholder="MM/YY" class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-slate-400 mb-1">CVV</label>
                      <input type="password" v-model="pago.cvv" maxlength="4" class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
                    </div>
                  </div>
                </div>

                <div v-if="pago.metodo === 'pago_movil'" class="space-y-4">
                  <div class="bg-emerald-900/20 border border-emerald-500/30 p-3 rounded-lg mb-4">
                    <p class="text-emerald-400 text-sm font-semibold">Datos para transferir:</p>
                    <p class="text-slate-300 text-sm">0414-1234567 • V-12345678 • Banco Mercantil</p>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-1">Banco Emisor</label>
                    <select v-model="pago.banco_origen" class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
                      <option value="" disabled>Selecciona tu banco</option>
                      <option v-for="banco in bancosVenezuela" :key="banco" :value="banco">{{ banco }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-1">Teléfono Origen</label>
                    <input type="tel" v-model="pago.telefono_origen" placeholder="0412..." class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-1">Número de Referencia (Últimos dígitos)</label>
                    <input type="text" v-model="pago.referencia" class="w-full rounded-md border border-slate-700 bg-slate-800 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-mono text-emerald-400">
                  </div>
                </div>

                <div v-if="pago.metodo === 'efectivo'" class="flex flex-col items-center justify-center h-48 text-center space-y-3">
                  <div class="text-4xl">💵</div>
                  <p class="text-slate-300">El cobro se realizará en efectivo al momento de la entrega o en caja.</p>
                  <p class="text-sm text-slate-500">Por favor tenga el monto exacto si es posible.</p>
                </div>

                <div class="mt-8 pt-4 border-t border-slate-700">
                  <button 
                    @click="procesarPago"
                    :disabled="procesando"
                    class="w-full py-3 px-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-lg shadow-md hover:shadow-lg transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ procesando ? 'Procesando...' : 'Confirmar Pago' }}
                  </button>
                </div>

              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  </div>
</template>