<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  productos: {
    type: Array,
    default: () => []
  },
  titulo: {
    type: String,
    default: "Mi Carrito"
  }
})

// Emits
const emit = defineEmits(['close', 'seleccionar', 'actualizar-cantidad', 'eliminar-producto'])

// Estado reactivo
const productoSeleccionado = ref(null)

// Métodos
const closeModal = () => {
  emit('close')
  resetModal()
}

const seleccionarProducto = (producto) => {
  productoSeleccionado.value = producto
  emit('seleccionar', producto)
}

const resetModal = () => {
  productoSeleccionado.value = null
}

// Incrementar cantidad
const incrementarCantidad = (producto) => {
  const nuevaCantidad = producto.cantidad + 1
  emit('actualizar-cantidad', { 
    producto, 
    nuevaCantidad 
  })
}

// Decrementar cantidad
const decrementarCantidad = (producto) => {
  if (producto.cantidad > 1) {
    const nuevaCantidad = producto.cantidad - 1
    emit('actualizar-cantidad', { 
      producto, 
      nuevaCantidad 
    })
  }
}

// Eliminar producto
const eliminarProducto = (producto) => {
  emit('eliminar-producto', producto)
}

// Actualizar cantidad manualmente
const actualizarCantidad = (producto, event) => {
  const nuevaCantidad = parseInt(event.target.value) || 1
  if (nuevaCantidad > 0) {
    emit('actualizar-cantidad', { 
      producto, 
      nuevaCantidad 
    })
  }
}

// Formatear precio
const formatearPrecio = (precio) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'USD'
  }).format(precio)
}

// Calcular total
const total = computed(() => {
  return props.productos.reduce((sum, producto) => sum + (producto.precio * producto.cantidad), 0)
})

// Calcular cantidad total de productos
const cantidadTotal = computed(() => {
  return props.productos.reduce((sum, producto) => sum + producto.cantidad, 0)
})

// Cerrar modal con ESC
const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.show) {
    closeModal()
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <Transition
    enter-active-class="transition-opacity duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-300"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      @click.self="closeModal"
    >
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition-all duration-300"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          class="w-full max-w-xl bg-slate-900 text-slate-100 rounded-2xl shadow-2xl overflow-hidden border border-slate-700"
        >
          <!-- Header -->
          <div class="bg-slate-800 border-b border-slate-700 p-6">
            <div class="flex justify-between items-center">
              <div>
                <h2 class="text-2xl font-bold">{{ titulo }}</h2>
                <p class="text-sm text-slate-400 mt-1">
                  {{ cantidadTotal }} producto{{ cantidadTotal !== 1 ? 's' : '' }} en total
                </p>
              </div>
              <button
                @click="closeModal"
                class="text-slate-400 hover:text-slate-100 transition-colors p-2 rounded-lg hover:bg-slate-700"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Contenido -->
          <div class="max-h-96 overflow-y-auto">
            <!-- Lista vacía -->
            <div 
              v-if="productos.length === 0"
              class="text-center py-12 text-slate-500"
            >
              <svg class="w-16 h-16 mx-auto text-slate-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
              <p class="text-lg text-slate-300">No hay productos en el carrito</p>
            </div>

            <!-- Lista de productos -->
            <div v-else class="divide-y divide-slate-800">
              <div
                v-for="(producto, index) in productos"
                :key="producto.id || index"
                class="p-4 transition-colors"
                :class="[
                  'hover:bg-slate-800/80',
                  productoSeleccionado?.id === producto.id
                    ? 'bg-slate-800 border-l-4 border-emerald-500'
                    : 'bg-slate-900'
                ]"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-4 flex-1">
                    <!-- Información del producto -->
                    <div class="flex-1">
                      <div class="flex justify-between items-start">
                        <div>
                          <h3 class="font-semibold text-slate-100">{{ producto.nombre }}</h3>
                        </div>
                        <button
                          @click="eliminarProducto(producto)"
                          class="text-slate-500 hover:text-red-400 transition-colors p-1"
                          title="Eliminar producto"
                        >
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                      
                      <div class="flex items-center justify-between mt-3">
                        <!-- Controles de cantidad -->
                        <div class="flex items-center space-x-3">
                          <span class="text-sm text-slate-400 font-medium">Cantidad:</span>
                          <div class="flex items-center border border-slate-600 rounded-lg bg-slate-900">
                            <button
                              @click="decrementarCantidad(producto)"
                              class="px-3 py-1 text-slate-300 hover:bg-slate-800 transition-colors rounded-l-lg"
                              :disabled="producto.cantidad <= 1"
                              :class="{
                                'opacity-40 cursor-not-allowed': producto.cantidad <= 1
                              }"
                            >
                              -
                            </button>
                            <input
                              type="number"
                              :value="producto.cantidad"
                              @change="actualizarCantidad(producto, $event)"
                              min="1"
                              class="w-12 text-center border-x border-slate-600 py-1 bg-slate-900 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                            />
                            <button
                              @click="incrementarCantidad(producto)"
                              class="px-3 py-1 text-slate-300 hover:bg-slate-800 transition-colors rounded-r-lg"
                            >
                              +
                            </button>
                          </div>
                        </div>

                        <!-- Precios -->
                        <div class="text-right">
                          <div class="text-sm text-slate-400">
                            {{ formatearPrecio(producto.precio) }} c/u
                          </div>
                          <div class="text-lg font-bold text-emerald-400">
                            {{ formatearPrecio(producto.precio * producto.cantidad) }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer con total -->
          <div 
            v-if="productos.length > 0"
            class="bg-slate-900 border-t border-slate-800 p-6"
          >
            <div class="flex justify-between items-center">
              <div>
                <p class="text-sm text-slate-400">
                  Total ({{ cantidadTotal }} producto{{ cantidadTotal !== 1 ? 's' : '' }})
                </p>
                <p class="text-2xl font-bold text-slate-100">{{ formatearPrecio(total) }}</p>
              </div>
              <div class="space-x-3">
                <button
                  @click="closeModal"
                  class="px-6 py-2 rounded-lg font-semibold text-slate-200 bg-slate-800 border border-slate-600 hover:bg-slate-700 transition-colors"
                >
                  Continuar comprando
                </button>
                <button
                  class="px-6 py-2 rounded-lg font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition-colors shadow-sm hover:shadow-md"
                >
                  Finalizar compra
                </button>
              </div>
            </div>
          </div>

          <!-- Footer sin productos -->
          <div 
            v-else
            class="bg-slate-900 border-t border-slate-800 p-6"
          >
            <button
              @click="closeModal"
              class="w-full px-6 py-2 rounded-lg font-semibold text-slate-200 bg-slate-800 border border-slate-600 hover:bg-slate-700 transition-colors"
            >
              Continuar comprando
            </button>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>