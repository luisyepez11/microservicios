<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const generarCodigo = () => {
  return Math.floor(100000 + Math.random() * 900000).toString()
}
const codigo = ref(generarCodigo())

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

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

const reenviarCodigo = () => {
  codigo.value = generarCodigo()
  tiempoRestante.value = 60
  codigoExpirado.value = false
  ingresarCodigo.value = ''
  errorCodigo.value = ''
  mensaje.value = ''
  startTimer()

  fetch('http://localhost:8001/codigo/reenviar', { // CAMBIAR RUTA
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code: codigo.value,
    }),
  }).catch(() => {})
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

  try {
    const res = await fetch('http://localhost:8001/codigo', { // CAMBIAR RUTA
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: ingresarCodigo.value,
      }),
    })

    if (!res.ok) {
      errorCodigo.value = 'Código incorrecto o expirado.'
      return
    }

    mensaje.value = 'Código verificado correctamente.'
    router.push('/login')
  } catch (err) {
    errorCodigo.value = 'No se pudo verificar el código.'
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center">
    <div class="w-full max-w-md bg-slate-800/80 rounded-2xl shadow-xl p-8 text-slate-100">
      <h1 class="text-2xl font-semibold mb-2 text-center">
        Hemos enviado un código a su correo electrónico
      </h1>
      <p class="text-sm text-slate-400 mb-6 text-center">
        Por favor verifique los dígitos.
      </p>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-sm mb-1" for="codigo">Ingrese el código</label>
          <input
            id="codigo"
            v-model="ingresarCodigo"
            type="text"
            class="w-full px-3 py-2 rounded-lg border focus:outline-none"
            placeholder="******"
          />
          <p v-if="errorCodigo" class="text-xs text-red-500 mt-1">
            {{ errorCodigo }}
          </p>

          <p class="text-xs text-slate-400 mt-1">
            Código expira en:
            <span
              :class="codigoExpirado ? 'text-red-400 font-mono' : 'text-emerald-400 font-mono'"
            >
              {{ tiempoFormateado }}
            </span>
          </p>

          <button
            type="button"
            class="mt-2 text-xs text-emerald-400 hover:underline disabled:opacity-40 disabled:cursor-not-allowed"
            :disabled="!codigoExpirado"
            @click="reenviarCodigo"
          >
            Reenviar código
          </button>
        </div>

        <p v-if="mensaje" class="text-sm text-emerald-400">
          {{ mensaje }}
        </p>

        <button
          type="submit"
          class="w-full py-2 rounded-lg font-semibold bg-emerald-500 hover:bg-emerald-400 transition"
        >
          Confirmar código
        </button>
      </form>
    </div>
  </div>
</template>