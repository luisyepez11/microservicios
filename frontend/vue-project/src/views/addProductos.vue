<script setup>
import { ref } from 'vue'
import sideBar from '@/components/sideBar.vue'
import NavBar from '@/components/navBar.vue'
import axios from 'axios'
import Clientesupabase from '@/clienteSupabes'

const usuario = ref('Usuario')
const fechaActual = ref(new Date().toLocaleDateString())

const fileInput = ref(null)
const imagePreview = ref(null)

const producto = ref({
 nombre: '',
 precio: 0,
 cantidad: 0,
 descripcion: '',

 imagen: null 
})

const triggerFileInput = () => {
 fileInput.value.click()
}

const handleImageUpload = (event) => {
 const file = event.target.files[0]
 if (file) {
  if (!file.type.match('image.*')) {
   alert('Por favor, selecciona un archivo de imagen válido.')
   return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
   // Usa la URL Base64 para la vista previa
   imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
  
  // Almacena el objeto File para el envío con FormData
  producto.value.imagen = file 
 }
}

const subirImagenes = async (imagenData) => {
  try {
    let file;
    
    if (typeof imagenData === 'string' && imagenData.startsWith('data:image')) {
      const base64Data = imagenData.split(',')[1];
      const binaryData = atob(base64Data);
      const arrayBuffer = new ArrayBuffer(binaryData.length);
      const uint8Array = new Uint8Array(arrayBuffer);
      
      for (let i = 0; i < binaryData.length; i++) {
        uint8Array[i] = binaryData.charCodeAt(i);
      }
      const blob = new Blob([uint8Array], { type: 'image/png' });
      file = new File([blob], 'producto.png', { type: 'image/png' });
    } else if (imagenData instanceof File) {
      file = imagenData;
    } else {
      console.error('Formato de imagen no soportado');
      return null;
    }
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 15);
    const fileExt = file.name.split('.').pop() || 'png';
    const fileName = `${timestamp}_${random}.${fileExt}`;
    const filePath = `productos/${fileName}`;

    console.log('Subiendo imagen:', fileName);

    const { data, error } = await Clientesupabase.storage
      .from('productos')
      .upload(filePath, file, {
        cacheControl: '3600',
        upsert: false
      });

    if (error) {
      console.error('Error de storage:', error);
      throw error;
    }

    const { data: { publicUrl } } = Clientesupabase.storage
      .from('productos')
      .getPublicUrl(filePath);

    console.log('Imagen subida:', publicUrl);
    return publicUrl;

  } catch (error) {
    console.error('Error subiendo imagen:', error.message);
    alert(`Error al subir imagen: ${error.message}`);
    return null;
  }
};

const guardarProducto = async () => {
 if (!producto.value.nombre || !producto.value.precio || !producto.value.cantidad) {
  alert('Por favor, completa los campos obligatorios: Nombre, Precio y Cantidad.')
  return
 }
 const formData = new FormData()
 formData.append('name', producto.value.nombre)
 formData.append('category_id', 1489)
 formData.append('price', producto.value.precio)
 formData.append('description', producto.value.descripcion)
 formData.append('cantidad', producto.value.cantidad) 
 
 if (producto.value.imagen) {
  const url_imagen = await subirImagenes(producto.value.imagen)
  formData.append('image_url', url_imagen)
 }
 
 try {
  const tokenGuardado = localStorage.getItem('authToken')
  

   const response = await axios.post(
   "http://localhost:8000/api/products/new",
   formData, 
   {
    headers: {
     'Authorization': `Bearer ${tokenGuardado}`,
    }
   }
  )
  console.log('Producto guardado:', response.data)
  const stock = await axios.post(
    'http://localhost:8003/api',{
      id_producto:response.data,
    cantidad:producto.value.cantidad
    })
    
  console.log('Producto guardado:', response.data)
  alert('Producto guardado exitosamente!')
  
  resetForm()
  
 } catch (error) {
  console.error('Error al guardar el producto:', error.response || error)
  const errorMessage = error.response?.data?.message || 'Error al guardar el producto (500). Revisa los logs de Laravel.'
  alert(errorMessage)
 }
}

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
  // NOTA: Si sigue dando 401, el token guardado no es válido para este endpoint.
  try {
    const response = await axios.get("http://127.0.0.1:8001/mi-perfil", {
      headers: {
        'Authorization': `Bearer ${tokenGuardado}`
      }
    })
    console.log(response.data)
  } catch (error) {
    console.log("Error 401 al cargar perfil: ", error) 
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
       
              <div class="flex flex-col items-center">
        <div
         class="w-80 h-80 bg-slate-900 border border-slate-700 rounded-xl flex items-center justify-center mb-4 overflow-hidden">
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