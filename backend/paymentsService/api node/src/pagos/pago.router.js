import { RegistrarPago,PagosUsuario,PagosTotales } from "./pago.controller.js";
import { Router } from "express";

const routerPagos = Router();

routerPagos.post('/',RegistrarPago)
routerPagos.get('/:id',PagosUsuario)
routerPagos.get('/',PagosTotales)
export default routerPagos;

