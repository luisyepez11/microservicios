<script setup>
import AddProductos from '@/views/addProductos.vue';

// Define las props
defineProps({
  textoBoton: {
    type: String,
    default: 'Comprar' // Valor por defecto
  },
  nombre:{
    type:String,
    default:"producto"
  },
  precio:{
    default:0.0
  },
  agregar:{
    type:Function,
    default:()=>{console.log("hola")}
  },
  producto:{
    type:Object,
    default:{}
  }
})
</script>
<template>
  <div 
    class="bg-slate-800/80 rounded-2xl shadow-xl border border-slate-700 overflow-hidden max-w-xs mx-auto text-slate-100"
  >
    <div
      class="w-full aspect-square bg-slate-900 flex items-center justify-center overflow-hidden"
    >
      <img
        :src= "producto.image_url"
        alt="Dos peras en un fondo blanco"
        class="w-full h-full object-cover"
      >
    </div>

    <div class="p-4">
      <h2 class="text-3xl font-normal text-slate-100 mb-1">
        {{ nombre }}
      </h2>

      <p class="text-2xl font-normal text-slate-300 mb-4">
        ${{ precio }}
      </p>
      <p class=" font-normal text-slate-300 mb-4">
        Cantidad : {{ producto.stock }}
      </p>
      <button
        class="w-full px-4 py-2 rounded-lg text-base font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition duration-150 ease-in-out shadow-sm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-60"
       @click="agregar(producto)"
        >
        {{ textoBoton }}
      </button>
    </div>
  </div>
</template>

