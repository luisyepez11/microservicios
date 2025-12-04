<template>
  <nav
    class="bg-slate-900 text-slate-100 w-40 flex flex-col items-center py-8 fixed top-0 bottom-0 left-0 z-10 shadow-lg border-r border-slate-800"
  >
    <div class="font-bold text-2xl mb-12 text-slate-100"></div>

    <ul class="flex flex-col items-center w-full gap-2">
      <li
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/home"
        >
          Principal
        </a>
      </li>
      <li
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/product"
        >
          Productos
        </a>
      </li>
      <li
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/stock"
        >
          Almacen
        </a>
      </li>
      <li
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/user"
        >
          Usuarios
        </a>
         <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/user"
        >
        </a>
      </li>
        <li
        class="w-full rounded-lg mx-2 hover:bg-slate-800 transition-colors duration-200"
      >
        <a
          class="no-underline block py-3 px-6 text-center font-medium text-slate-100 hover:text-emerald-400"
          href="http://localhost:5173/gestion_producto"
        >
          Gestion Producto
        </a>
      </li>
    </ul>
  </nav>
</template>