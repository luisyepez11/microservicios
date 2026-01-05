<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  correo: {
    type: String,
    default: ""
  }
})

const emit = defineEmits(['close', 'verified'])

const codigo = ref('')
const ingresarCodigo = ref('')
const errorCodigo = ref('')
const mensaje = ref('')
const tiempoRestante = ref(60)
const codigoExpirado = ref(false)
let intervalId = null

const tiempoFormateado = computed(() => {
  const m = Math.floor(tiempoRestante.value / 60).toString().padStart(2, '0')
  const s = (tiempoRestante.value % 60).toString().padStart(2, '0')
  return `${m}:${s}`
})

const generarCodigo = () => {
  return Math.floor(100000 + Math.random() * 900000).toString()
}

const enviarCodigoCorreo = async () => {
  if (!props.correo) {
    console.error('No hay correo proporcionado')
    return
  }
  console.log(codigo.value)
  try {
    const res = await fetch('http://localhost:8001/enviar-codigo-verificacion', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "correo_usuario": props.correo,
        "codigo_verificacion": codigo.value
      }),
    })
    
    if (res.ok) {
      console.log('Código enviado correctamente')
    } else {
      console.error('Error al enviar código')
    }
  } catch (error) {
    console.error('Error de conexión:', error)
  }
}

const startTimer = () => {
  if (intervalId) clearInterval(intervalId)

  intervalId = setInterval(() => {
    if (tiempoRestante.value > 0) {
      tiempoRestante.value--
    } else {
      codigoExpirado.value = true
      clearInterval(intervalId)
      intervalId = null
      errorCodigo.value = 'El código ha expirado. Reenvíalo para generar uno nuevo.'
    }
  }, 1000)
}

const inicializarModal = async () => {
  codigo.value = generarCodigo()
  tiempoRestante.value = 60
  codigoExpirado.value = false
  ingresarCodigo.value = ''
  errorCodigo.value = ''
  mensaje.value = ''
  
  await enviarCodigoCorreo()
  
  startTimer()
}

const reenviarCodigo = async () => {
  await inicializarModal()
}

const onSubmit = async () => {
  errorCodigo.value = ''
  mensaje.value = ''

  if (!ingresarCodigo.value) {
    errorCodigo.value = 'Ingrese el código que enviamos a su correo.'
    return
  }

  if (codigoExpirado.value) {
    errorCodigo.value = 'El código ha expirado. Reenvíalo para generar uno nuevo.'
    return
  }

  if (ingresarCodigo.value !== codigo.value) {
    errorCodigo.value = 'El código ingresado no es correcto.'
    return
  }

  if(ingresarCodigo.value!==codigo.value){
      return
  }

    mensaje.value = 'Código verificado correctamente.'
    emit('verified')
    closeModal()
}

const closeModal = () => {
  emit('close')
  resetModal()
}

const resetModal = () => {
  ingresarCodigo.value = ''
  errorCodigo.value = ''
  mensaje.value = ''
  tiempoRestante.value = 60
  codigoExpirado.value = false
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.show) {
    closeModal()
  }
}

watch(() => props.show, async (newVal) => {
  if (newVal) {
    await inicializarModal()
  }
})

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  if (intervalId) clearInterval(intervalId)
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
          class="w-full max-w-md bg-slate-800/90 rounded-2xl shadow-2xl p-8 text-slate-100 border border-slate-700/50"
        >
          <!-- Header -->
          <div class="flex justify-between items-start mb-4">
            <div>
              <h2 class="text-2xl font-semibold mb-2">
                Verificación de código
              </h2>
              <p class="text-sm text-slate-400">
                Hemos enviado un código a: <br>
                <span class="text-emerald-400">{{ correo }}</span>
              </p>
            </div>
            <button
              @click="closeModal"
              class="text-slate-400 hover:text-slate-200 transition-colors p-1 rounded-lg hover:bg-slate-700/50"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Form -->
          <form @submit.prevent="onSubmit" class="space-y-4">
            <div>
              <label class="block text-sm mb-1" for="codigo">Ingrese el código</label>
              <input
                id="codigo"
                v-model="ingresarCodigo"
                type="text"
                maxlength="6"
                class="w-full px-3 py-2 rounded-lg border border-slate-600 bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-white placeholder-slate-400"
                placeholder="******"
              />
              <p v-if="errorCodigo" class="text-xs text-red-400 mt-1">
                {{ errorCodigo }}
              </p>

              <div class="flex justify-between items-center mt-2">
                <p class="text-xs text-slate-400">
                  Código expira en:
                  <span
                    :class="codigoExpirado ? 'text-red-400 font-mono' : 'text-emerald-400 font-mono'"
                  >
                    {{ tiempoFormateado }}
                  </span>
                </p>

                <button
                  type="button"
                  class="text-xs text-emerald-400 hover:text-emerald-300 underline disabled:opacity-40 disabled:cursor-not-allowed disabled:no-underline transition-colors"
                  :disabled="!codigoExpirado"
                  @click="reenviarCodigo"
                >
                  Reenviar código
                </button>
              </div>
            </div>

            <p v-if="mensaje" class="text-sm text-emerald-400">
              {{ mensaje }}
            </p>

            <div class="flex gap-3 pt-2">
              <button
                type="button"
                @click="closeModal"
                class="flex-1 py-2 rounded-lg font-semibold bg-slate-600 hover:bg-slate-500 transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="flex-1 py-2 rounded-lg font-semibold bg-emerald-500 hover:bg-emerald-400 transition-colors"
              >
                Confirmar
              </button>
            </div>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>