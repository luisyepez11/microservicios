<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios';
const router = useRouter()

const email = ref('')
const contrasena = ref('')
const mostrarContrasena = ref(false)

const errorEmail = ref('')
const errorContrasena = ref('')
const errorGeneral = ref('')

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
  if (value.length < 9) {
    return 'La contraseña debe tener al menos 9 caracteres.'
  }
  return ''
}

const validarFormulario = () => {
  errorEmail.value = validarEmail(email.value)
  errorContrasena.value = validarContrasena(contrasena.value)

  return !errorEmail.value && !errorContrasena.value
}

const onSubmit = async () => {
  errorGeneral.value = ''

  const valido = validarFormulario()
  if (!valido) return

  try {
    let res = await axios.post('http://127.0.0.1:8001/login', {
            correo_usuario: email.value,
            contraseña_usuario: contrasena.value
        });

         let tokend = res.data.access_token
         localStorage.setItem('authToken', tokend);
        router.push({
            name: 'home'
        });

    if (!res.ok) {
      errorGeneral.value = 'Credenciales inválidas o error en el servidor.'
      return
    }


    router.push('/products')
  } catch (err) {
    errorGeneral.value = err
  }
}
</script>

<template>
    <div class="min-h-screen bg-slate-900 flex items-center justify-center">
  <div class="w-full max-w-md bg-slate-800/80 rounded-2xl shadow-xl p-8 text-slate-100">
    <h1 class="text-2xl font-semibold mb-2 text-center">Iniciar sesión</h1>
    <p class="text-sm text-slate-400 mb-6 text-center">
      Ingresa tu correo y contraseña para iniciar sesión.
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
        <label class="block text-sm mb-1" for="contrasena">Contraseña</label>
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

        <p v-if="errorContrasena" class="text-xs text-red-400 mt-1">
          {{ errorContrasena }}
        </p>
      </div>

      <p v-if="errorGeneral" class="text-sm text-red-400">
        {{ errorGeneral }}
      </p>

      <button
        type="submit"
        class="w-full py-2 rounded-lg font-semibold bg-emerald-500 text-slate-950 hover:bg-emerald-400 active:scale-[0.98] transition"
      >
        Iniciar sesión
      </button>
    </form>

    <p class="mt-4 text-sm text-center text-slate-300">
      ¿No tienes una cuenta?
      <router-link to="/register" class="text-emerald-400 hover:underline">
        Regístrate aquí
      </router-link>
    </p>
  </div>
  </div>
</template>