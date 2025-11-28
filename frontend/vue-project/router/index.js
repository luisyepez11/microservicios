// src/router/index.js

import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/home.vue";
import Login from "@/views/login.vue";
import Register from "@/views/register.vue";
import Usuarios from "@/views/usuarios.vue";
import Productos from "@/views/productos.vue";
import Stock from "@/views/stock.vue";
import AddProductos from "@/views/addproductos.vue";
import Codigo from '../src/views/codigo.vue';

const routes = [
    {
        path: '/',
        name: 'login',
        component: Login
    },
    {
        path: '/register',
        name: 'register',
        component: Register
    },
    {
        path: '/home',
        name: 'home',
        component: Home
    },
    {
        path: '/user',
        name: 'user',
        component: Usuarios
    },
    {
        path: '/product',
        name: 'product',
        component: Productos
    },
    {
        path: '/stock',
        name: 'stock',
        component: Stock
    },
    {
        path: '/add-product',
        name: 'add-product',
        component: AddProductos
    },
    {
        path: '/codigo',
        name: 'codigo',
        component: Codigo
    }
];

const router = createRouter({
    history: createWebHistory(), 
    routes
});

export default router;