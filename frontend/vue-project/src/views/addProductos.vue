<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios'

const usuario = ref('Usuario')
const fechaActual = ref(new Date().toLocaleDateString())

// Referencias para el input de archivo y la vista previa
const fileInput = ref(null)
const imagePreview = ref(null)

// Datos del producto
const producto = ref({
  nombre: '',
  precio: 0,
  cantidad: 0,
  descripcion: '',
  imagen: null
})

// Función para abrir el selector de archivos
const triggerFileInput = () => {
  fileInput.value.click()
}

// Función para manejar la subida de imagen
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validar que sea una imagen
    if (!file.type.match('image.*')) {
      alert('Por favor, selecciona un archivo de imagen válido.')
      return
    }
    
    // Crear una URL local para la vista previa
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
    
    // Guardar el archivo para enviarlo al servidor
    producto.value.imagen = file
  }
}

// Función para guardar el producto
const guardarProducto = async () => {
  // Validar campos obligatorios
  if (!producto.value.nombre || !producto.value.precio || !producto.value.cantidad) {
    alert('Por favor, completa los campos obligatorios: Nombre, Precio y Cantidad.')
    return
  }
  
  try {
    const tokenGuardado = localStorage.getItem('authToken')
    
    // Crear FormData para enviar la imagen
    const formData = new FormData()
    formData.append('nombre', producto.value.nombre)
    formData.append('precio', producto.value.precio)
    formData.append('cantidad', producto.value.cantidad)
    formData.append('descripcion', producto.value.descripcion)
    
    if (producto.value.imagen) {
      formData.append('imagen', producto.value.imagen)
    }
    
    // Enviar datos al servidor
    const response = await axios.post("http://127.0.0.1:8001/productos", formData, {
      headers: {
        'Authorization': `Bearer ${tokenGuardado}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    console.log('Producto guardado:', response.data)
    alert('Producto guardado exitosamente!')
    
    // Limpiar formulario después de guardar
    resetForm()
    
  } catch (error) {
    console.error('Error al guardar el producto:', error)
    alert('Error al guardar el producto. Por favor, intenta nuevamente.')
  }
}

// Función para resetear el formulario
const resetForm = () => {
  producto.value = {
    nombre: '',
    precio: 0,
    cantidad: 0,
    descripcion: '',
    imagen: null
  }
  imagePreview.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const cerrarSesion = () => {
    localStorage.removeItem('authToken');
}

const tokenGuardado = localStorage.getItem('authToken');
const cargar = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:8001/mi-perfil", {
            headers: {
                'Authorization': `Bearer ${tokenGuardado}`
            }
        })
        console.log(response.data)
    } catch (error) {
        console.log(error)
    }
}
cargar()
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex text-slate-100">
    <sideBar></sideBar>
    
    <div class="flex-1 ml-40">
      <NavBar></NavBar>
      
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <h1 class="text-2xl font-bold text-slate-100 mb-6">Añadir Producto</h1>
          
          <div class="bg-slate-800/80 shadow-xl rounded-2xl p-6 border border-slate-700">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              <!-- Lado imagen -->
              <div class="flex flex-col items-center">
                <div
                  class="w-80 h-80 bg-slate-900 border border-slate-700 rounded-xl flex items-center justify-center mb-4 overflow-hidden"
                >
                  <img 
                    v-if="imagePreview" 
                    :src="imagePreview" 
                    alt="Vista previa" 
                    class="w-full h-full object-cover"
                  >
                  <span v-else class="text-slate-500 text-center p-4">
                    Imagen del Producto
                  </span>
                </div>

                <input 
                  type="file" 
                  ref="fileInput"
                  @change="handleImageUpload"
                  class="hidden"
                  accept="image/*"
                >
                <button 
                  class="px-4 py-2 rounded-lg font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition shadow-sm hover:shadow-md"
                  @click="triggerFileInput"
                >
                  Subir Imagen
                </button>
              </div>
              
              <!-- Lado formulario -->
              <div class="space-y-6">
                <div>
                  <label for="nombre" class="block text-sm font-medium text-slate-200 mb-1">
                    Nombre Producto:
                  </label>
                  <input 
                    type="text" 
                    id="nombre" 
                    v-model="producto.nombre"
                    class="w-full rounded-md border border-slate-700 bg-slate-900 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    placeholder="Ingrese el nombre del producto"
                  >
                </div>
                
                <div>
                  <label for="precio" class="block text-sm font-medium text-slate-200 mb-1">
                    Precio Producto:
                  </label>
                  <input 
                    type="number" 
                    id="precio" 
                    v-model="producto.precio"
                    step="0.01" 
                    min="0"
                    class="w-full rounded-md border border-slate-700 bg-slate-900 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    placeholder="0.00"
                  >
                </div>
                
                <div>
                  <label for="cantidad" class="block text-sm font-medium text-slate-200 mb-1">
                    Cantidad de ingresos de Producto:
                  </label>
                  <input 
                    type="number" 
                    id="cantidad" 
                    v-model="producto.cantidad"
                    min="0"
                    class="w-full rounded-md border border-slate-700 bg-slate-900 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    placeholder="0"
                  >
                </div>
                
                <div>
                  <label for="descripcion" class="block text-sm font-medium text-slate-200 mb-1">
                    Descripción:
                  </label>
                  <textarea 
                    id="descripcion" 
                    rows="4"
                    v-model="producto.descripcion"
                    class="w-full rounded-md border border-slate-700 bg-slate-900 text-slate-100 shadow-sm py-2 px-3 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    placeholder="Ingrese la descripción del producto"
                  ></textarea>
                </div>
                
                <div class="pt-4 flex justify-center">
                  <button 
                    class="px-6 py-2 rounded-lg font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition shadow-sm hover:shadow-md"
                    @click="guardarProducto"
                  >
                    Guardar Producto
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