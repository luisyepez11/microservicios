import { pool } from "../db.js";

export const RegistrarPago = async (req,res) => {
    try {
        const {idPedido,idUsuario,fechaPago,MontoPagado,metodoPago} = req.body
        const result = await pool.query(`INSERT INTO pagos (id_pedido,id_usuario,fecha_pago,metodo_pago,monto_pago) VALUES($1,$2,$3,$4,$5) RETURNING id_pago`,[idPedido,idUsuario,fechaPago,metodoPago,MontoPagado])
        res.status(201).json({
            message:"pago realizado",
            id_pago:result.rows[0].id_pago
        })
    } catch (error) {
        console.log(error)
        res.status(400).json({
            message:error
        })
    }
}

export const PagosUsuario = async (req,res) => {
    try {
        const idUsuario = req.params.id
        const result = await pool.query(`SELECT * FROM pagos WHERE id_usuario = $1 `,[idUsuario])
        res.status(201).json(result.rows)
    } catch (error) {
        res.status(400).json({
            message:error
        })
    }
}

export const PagosTotales= async (req,res) => {
    try {
        const result = await pool.query(`SELECT * FROM pagos  `)
        res.status(201).json(result.rows)
    } catch (error) {
        res.status(400).json({
            message:error
        })
    }
}