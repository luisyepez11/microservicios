package com.ordersService.ordersService.service;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ordersService.ordersService.model.Pedidos;
import com.ordersService.ordersService.model.PedidosProductos;
import com.ordersService.ordersService.model.PedidosProductosDTO;
import com.ordersService.ordersService.repository.PedidosProductosRepository;
import com.ordersService.ordersService.repository.PedidosRepository;

import jakarta.transaction.Transactional;

@Service
public class PedidosProductosServicio {
    @Autowired
    private PedidosProductosRepository repositorioPedidosProductos;
    @Autowired
    private PedidosRepository repositorioPedidos;

    public  List<PedidosProductos> allPedidos(){
        return  repositorioPedidosProductos.findAll();
    }

    public List<PedidosProductos> pedidosProducto(UUID idPedido){
        return  repositorioPedidosProductos.findByPedidos_IdPedido(idPedido);
    }

    @Transactional
    public List<PedidosProductos>  productosPedidos(List<PedidosProductosDTO> productos,UUID idPedido){
        for (PedidosProductosDTO producto : productos) {
            Pedidos pedido = repositorioPedidos.getById(idPedido);
            PedidosProductos nuevaEntidad = new PedidosProductos();
            nuevaEntidad.setPedidos(pedido);
            nuevaEntidad.setIdProducto(producto.idProducto());
            nuevaEntidad.setCantidadProducto(producto.cantidadProducto());
            repositorioPedidosProductos.save(nuevaEntidad);
        }
        return repositorioPedidosProductos.findByPedidos_IdPedido(idPedido);
    }

    @Transactional
    public List<Object[]> cantidadPedidosProductos(){
        return repositorioPedidosProductos.countPedidosByProducto();
    }
}
