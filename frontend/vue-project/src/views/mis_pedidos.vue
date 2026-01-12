<script setup>
import { ref,onMounted } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios';
import Productos from './productos.vue';
const pedidos = ref({})
const fechaActual = ref(new Date().toLocaleDateString())
const usuario = ref('')
const estados = ref('')
const estadosPedidos = ref('file:///C:/Users/hp/Downloads/Gemini_Generated_Image_10c2hn10c2hn10c2.png')
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
    usuario.value = response.data
    const listaPedidos = await axios.get(`http://localhost:8080/pedidosUsuarios/${usuario.value.id_usuario}`)
    
    pedidos.value = listaPedidos.data;
    console.log(pedidos.value)
} catch (error) {
    console.log(error)
}
}
const simulacionPago = async (productosPnientes)=>{
  console.log(pedidos.value)
  const productosPendientes =await pedidos.value.map(p =>{
    if (p.estado==="PAGADO"){
        return p
    }
  })
  console.log(productosPendientes)
  estados.value = "Pago recibidos, pedido en proceso de envidó"
  await new Promise(resolve => setTimeout(resolve, 10000))
  estados.value = "Pedido enviado"
  await new Promise(resolve => setTimeout(resolve, 20000))
  estados.value = "Pedido ya en su destino"
  productosPendientes.map(async p=>{
    if (p !== undefined){
    const cambioEstado = await axios.put(`http://localhost:8080/entregarPedido/${p.idPedido}`)
    const notificacionEntrega = await axios.post(`http://localhost:8090/api/notificacion/entregado`,{
    correo:usuario.value.correo_usuario
    })
  }}
  )
}
onMounted(async() => {
  await cargar()
  simulacionPago();
});
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
                Encabezado 1
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider"
              >
                Encabezado 2
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider"
              >
                Encabezado 3
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr
              class="bg-slate-900/70 hover:bg-slate-800 transition duration-150"
              v-for="pedido in pedidos"
            >
              <td v-if="pedido.estado !=='PAGADO'" class="px-6 py-4 whitespace-nowrap text-sm text-slate-100" >
                <div class="text-3xl"> 🛒 </div>
              </td>
              <td v-if="pedido.estado ==='PAGADO'" class="px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                 <img v-if="estados ==='Pedido ya en su destino'" class="rounded-2xl " src='file:///C:/Users/hp/Downloads/Gemini_Generated_Image_10c2hn10c2hn10c2.png' alt="" width="100px">
                 <img v-if="estados ==='Pedido enviado'" class="rounded-2xl transform -scale-x-100" src='file:///C:/Users/hp/Downloads/pixverse_mp4_media_web_ori_4ad5ea0a-85b2-4e4f-8bea-9fb6f58ae3ae_seed616307380.gif' alt="" width="100px">
                 <img v-if="estados ==='Pago recibidos, pedido en proceso de envidó'" class="rounded-2xl transform -scale-x-100" src='file:///C:/Users/hp/Downloads/Reloj___%20GIF.gif' alt="" width="100px">
                 
              </td>
              <td v-if="pedido.estado ==='PAGADO'" class=" flex text-center px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                {{ estados }}
              </td>
              <td v-if="pedido.estado !=='PAGADO'" class=" flex text-center px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                {{ pedido.estado }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                <button
                  class="bg-emerald-500 text-slate-950 px-4 py-2 rounded-lg hover:bg-emerald-400 active:scale-[0.98] transition duration-150 font-semibold shadow-sm hover:shadow-md"
                >
                  ver
                </button>
              </td>
              <td v-if:="pedido.estado==='CREADO'" class="px-6 py-4 whitespace-nowrap text-sm text-slate-100">
                <router-link
                  :to="{ name: 'formulario_pago', params: { id: pedido.idPedido } }"
                >
                  <button
                  class="bg-emerald-500 text-slate-950 px-4 py-2 rounded-lg hover:bg-emerald-400 active:scale-[0.98] transition duration-150 font-semibold shadow-sm hover:shadow-md"
                >
                  Pagar
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