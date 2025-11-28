<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Codigo from './codigo.vue'
const router = useRouter()

const email = ref('')
const contrasena = ref('')
const confirmarContrasena = ref('')
const mostrarContrasena = ref(false)
const mostrarConfirmarContrasena = ref(false)

const errorEmail = ref('')
const errorContrasena = ref('')
const errorConfirmarContrasena = ref('')
const backendError = ref('')
const mensajeCompletado = ref('')
const showModal = ref(false)

const openModal = () => {
  showModal.value = true
}

const handleClose = () => {
  console.log('Modal cerrado')
  showModal.value = false
}

const handleVerified = async () => {
  console.log('Código verificado correctamente')
  try {
    const res = await fetch('http://localhost:8001/usuarios', { //CAMBIAR RUTA
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        correo_usuario: email.value,
        contraseña_usuario: contrasena.value,
      }),
    })

    if (!res.ok) {
      backendError.value = 'No se pudo registrar el usuario (quizás ya exista).'
      return
    }

    mensajeCompletado.value = 'Usuario registrado correctamente. Revisa tu correo para el código.'
    router.push('/')
  } catch (err) {
    backendError.value = 'Error al conectar con el servidor.'
  }
}

const validarEmail = (value) => {
  if (!value) {
    return 'Ingrese un correo.'
  }
  if (!value.includes('@')) {
    return 'El correo debe tener "@".'
  }
  if (!value.endsWith('.com')) {
    return 'El correo debe terminar en ".com".'
  }
  return ''
}

const validarContrasena = (value) => {
  if (!value) {
    return 'Ingrese una contraseña.'
  }
  if (value.length < 10) {
    return 'La contraseña debe tener al menos 10 caracteres.'
  }
  return ''
}

const validarConfirmacionContrasena = (contrasenaValue, confirmarValue) => {
  if (!confirmarValue) {
    return 'Debe confirmar la contraseña.'
  }
  if (contrasenaValue !== confirmarValue) {
    return 'Las contraseña y su confirmación no coinciden.'
  }
  return ''
}

const validarFormulario = () => {
  errorEmail.value = validarEmail(email.value)
  errorContrasena.value = validarContrasena(contrasena.value)
  errorConfirmarContrasena.value = validarConfirmacionContrasena(
    contrasena.value,
    confirmarContrasena.value
  )

  return !errorEmail.value && !errorContrasena.value && !errorConfirmarContrasena.value
}

const onSubmit = async () => {
  backendError.value = ''
  mensajeCompletado.value = ''

  const valido = validarFormulario()
  if (!valido) return
  openModal()

}
</script>

<template>
  <Codigo 
      :show="showModal" 
      @close="handleClose"
      @verified="handleVerified"
      :correo="email"
    />
    <div class="min-h-screen bg-slate-900 flex items-center justify-center">
  <div class="w-full max-w-md bg-slate-800/80 rounded-2xl shadow-xl p-8 text-slate-100">
    <h1 class="text-2xl font-semibold mb-2 text-center">Registro</h1>
    <p class="text-sm text-slate-400 mb-6 text-center">
      Crea tu cuenta con tu correo y una contraseña segura.
    </p>

    <form @submit.prevent="onSubmit" class="space-y-4">

      <div>
        <label class="block text-sm mb-1" for="email">Correo electrónico</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="w-full px-3 py-2 rounded-lg border focus:outline-none"
          placeholder="ejemplo@correo.com"
        />
        <p v-if="errorEmail" class="text-xs text-red-500 mt-1">
          {{ errorEmail }}
        </p>
      </div>

      <div>
        <label class="block text-sm mb-1" for="contrasena">Crear contraseña</label>
        <div class="relative">
          <input
            id="contrasena"
            v-model="contrasena"
            :type="mostrarContrasena ? 'text' : 'password'"
            class="w-full px-3 py-2 pr-10 rounded-lg bg-slate-900 border border-slate-700 text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            placeholder="Mínimo 10 caracteres"
          />
          <button
            type="button"
            class="absolute inset-y-0 right-2 flex items-center text-slate-400 hover:text-slate-200 text-xs"
            @click="mostrarContrasena = !mostrarContrasena"
          >
            {{ mostrarContrasena ? '🙈' : '👁️' }}
          </button>
        </div>
        <p v-if="errorContrasena" class="text-xs text-red-500 mt-1">
          {{ errorContrasena }}
        </p>
      </div>

      <div>
        <label class="block text-sm mb-1" for="confirmarContrasena">
          Confirmar contraseña
        </label>
        <div class="relative">
          <input
            id="confirmarContrasena"
            v-model="confirmarContrasena"
            :type="mostrarConfirmarContrasena ? 'text' : 'password'"
            class="w-full px-3 py-2 pr-10 rounded-lg bg-slate-900 border border-slate-700 text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            placeholder="Repite la contraseña"
          />
          <button
            type="button"
            class="absolute inset-y-0 right-2 flex items-center text-slate-400 hover:text-slate-200 text-xs"
            @click="mostrarConfirmarContrasena = !mostrarConfirmarContrasena"
          >
            {{ mostrarConfirmarContrasena ? '🙈' : '👁️' }}
          </button>
        </div>
        <p v-if="errorConfirmarContrasena" class="text-xs text-red-500 mt-1">
          {{ errorConfirmarContrasena }}
        </p>
      </div>

      <p v-if="backendError" class="text-sm text-red-500">
        {{ backendError }}
      </p>

      <p v-if="mensajeCompletado" class="text-sm text-emerald-400">
        {{ mensajeCompletado }}
      </p>

      <button
        type="submit"
        class="w-full py-2 rounded-lg font-semibold bg-emerald-500 hover:bg-emerald-400 transition"
      >
        Registrarse
      </button>
    </form>

    <p class="mt-4 text-sm text-center text-slate-300">
      ¿Ya tienes una cuenta?
      <router-link to="/" class="text-emerald-400 hover:underline">
        Inicia sesión aquí
      </router-link>
    </p>
  </div>
  </div>
</template>