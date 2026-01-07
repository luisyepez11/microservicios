<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import Card from '@/components/card.vue';
import axios from 'axios';
const usuario = ref('Usuario')
const fechaActual = ref(new Date().toLocaleDateString())
const listaProductos = ref({})
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
    const productos = await axios.get("http://localhost:8000/api/products")
    listaProductos.value = productos.data;
} catch (error) {
    console.log(error)
}
}
cargar()
const agregarAlCarrito = (producto) => {
  console.log(productos.value)
  const productoEnCarrito = productos.value.find(item => item.idProducto === producto.product_id)
  console.log(productoEnCarrito)
  if (productoEnCarrito) {
    // Si ya existe, verificar que no exceda el stock
    const cantidadProductoTotal = productoEnCarrito.cantidadProducto + (producto.cantidadProducto || 1)
    
    
    // Actualizar cantidadProducto
    productoEnCarrito.cantidadProducto = cantidadProductoTotal
    console.log(`Producto ${producto.nombre} actualizado en el carrito`)
  } else {
    // Si no existe, agregarlo al carrito
    const productoAAgregar = {
      ...{idProducto:producto.product_id,
        nombre:producto.name,
        precio:producto.price
      },
      cantidadProducto: producto.cantidadProducto || 1
    }
    
    productos.value.push(productoAAgregar)
    console.log(`Producto ${producto.name} agregado al carrito`)
    console.log(producto)
  }
  
  return true
}
const productos = ref([
])
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <!-- Sidebar -->
    <sideBar></sideBar>

    <!-- Main Content -->
    <div class="flex-1 ml-40">
      <!-- Navbar -->
      <NavBar :productos="productos"></NavBar>

      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="grid px-4 py-6 sm:px-0 grid-cols-5 gap-6">
          <Card v-for="value in listaProductos"
          :nombre="value.name" :precio="value.price" :agregar="agregarAlCarrito" :producto="value"></Card>
        </div>
      </main>
    </div>
  </div>
</template>