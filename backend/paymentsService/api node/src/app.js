import express, { json } from "express";
import cors from "cors";
import cookieParser from "cookie-parser";

const app = express();

//Middleware
app.use(cors({
    origin: '*',
    credentials: true
}))
app.use(json());
app.use(cookieParser());

//importaciones de rutas
//pagos
import RouterPagos from "./pagos/pago.router.js";

//rutas
//pagos
app.use("/api/pagos",RouterPagos)

export default app;