<template>
    <nav class="bg-[#E5E5E5] text-[#2C5282] w-40 flex flex-col items-center py-8 fixed top-0 bottom-0 left-0 z-10 shadow-lg">
        <div class="font-bold text-2xl mb-12 text-[#2C5282]"></div>

        <ul class="flex flex-col items-center w-full gap-2">
            <li class="w-full hover:bg-blue-100 transition-colors duration-200 rounded-lg mx-2">
                <a class="text-[#2C5282] no-underline block py-3 px-6 text-center font-medium hover:text-blue-700" href="http://localhost:5173/home"> Principal</a>
            </li>
            <li class="w-full hover:bg-blue-100 transition-colors duration-200 rounded-lg mx-2">
                <a class="text-[#2C5282] no-underline block py-3 px-6 text-center font-medium hover:text-blue-700" href="http://localhost:5173/product"> Productos</a>
            </li>
            <li class="w-full hover:bg-blue-100 transition-colors duration-200 rounded-lg mx-2">
                <a class="text-[#2C5282] no-underline block py-3 px-6 text-center font-medium hover:text-blue-700" href="http://localhost:5173/stock"> almacen</a>
            </li>
            <li class="w-full hover:bg-blue-100 transition-colors duration-200 rounded-lg mx-2">
                <a class="text-[#2C5282] no-underline block py-3 px-6 text-center font-medium hover:text-blue-700" href="http://localhost:5173/user"> Usuarios</a>
            </li>
        </ul>
    </nav>
</template>