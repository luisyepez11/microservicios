<script setup>
import { ref } from 'vue'
import axios from 'axios';
import Car from './car.vue' // Ajusta la ruta según tu estructura

// Estados para el carrito
const showModal = ref(false)
const productoSeleccionado = ref(null)
const props = defineProps({
  productos: {
    type: Array,
    default: () => []
  },

})

// Métodos del carrito
const openModal = () => {
  showModal.value = true
}

const handleClose = () => {
  showModal.value = false
}

const handleSeleccionar = (producto) => {
  productoSeleccionado.value = producto
  console.log('Producto seleccionado:', producto)
  showModal.value = false
}

const handleActualizarCantidad = ({ producto, nuevaCantidad }) => {
  const productoIndex = props.productos.findIndex(p => p.id === producto.id)
  console.log(productoIndex)
  if (productoIndex !== -1) {
    props.productos[productoIndex].cantidad = nuevaCantidad
    console.log(`Cantidad actualizada: ${producto.nombre} -> ${nuevaCantidad}`)
  }
}

const handleEliminarProducto = (producto) => {
  const productoIndex = props.productos.findIndex(p => p.id === producto.id)
  if (productoIndex !== -1) {
    props.productos.splice(productoIndex, 1)
    console.log(`Producto eliminado: ${producto.nombre}`)
  }
}

const cantidadTotalProductos = () => {
  return props.productos.reduce((sum, producto) => sum + producto.cantidad, 0)
}

const cerrarSesion = () => {
  localStorage.removeItem('authToken');
  window.location.href='http://localhost:5173'
}

</script>

<template>
  <header class="bg-slate-900 border-b border-slate-800 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center">
          <h1 class="text-2xl font-bold text-slate-100">
            Dashboard
          </h1>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-slate-100 font-medium">Hola</span>
          <button
            class="bg-emerald-500 text-slate-950 px-4 py-2 rounded-lg hover:bg-emerald-400 active:scale-[0.98] transition duration-150 font-semibold shadow-sm hover:shadow-md"
            @click="cerrarSesion"
          >
            Cerrar Sesión
          </button>
          <button
            class="bg-emerald-500 text-slate-950 px-4 py-2 rounded-lg hover:bg-emerald-400 active:scale-[0.98] transition duration-150 font-semibold shadow-sm hover:shadow-md relative"
            @click="openModal"
          >
            Carrito
            <!-- Badge con cantidad total de productos -->
            <span 
              v-if="cantidadTotalProductos() > 0"
              class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cantidadTotalProductos() }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal del Carrito -->
    <Car 
      :show="showModal" 
      :productos="props.productos"
      titulo="Mi Carrito de Compras"
      @close="handleClose"
      @seleccionar="handleSeleccionar"
      @actualizar-cantidad="handleActualizarCantidad"
      @eliminar-producto="handleEliminarProducto"
    />
  </header>
</template>