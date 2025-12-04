// src/router/index.js

import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/home.vue";
import Login from "@/views/login.vue";
import Register from "@/views/register.vue";
import Usuarios from "@/views/usuarios.vue";
import Productos from "@/views/productos.vue";
import Stock from "@/views/stock.vue";
import addproductos from "@/views/addProductos.vue";
import Codigo from '../src/views/codigo.vue';
import gestion_producto from "@/views/gestion_producto.vue";

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
        component: addproductos
    },
    {
        path: '/codigo',
        name: 'codigo',
        component: Codigo
    },{
        path: '/gestion_producto',
        name: 'gestion_producto',
        component: gestion_producto
    }
];

const router = createRouter({
    history: createWebHistory(), 
    routes
});

export default router;