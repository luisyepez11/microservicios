package com.ordersService.ordersService.controller;

import java.util.List;
import java.util.UUID;

import org.springframework.web.bind.annotation.RestController;

import com.ordersService.ordersService.model.PedidosProductos;
import com.ordersService.ordersService.model.PedidosProductosDTO;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import com.ordersService.ordersService.repository.PedidosProductosRepository;
import com.ordersService.ordersService.service.PedidosProductosServicio;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;



@RestController
public class PedidosProductosController {
    @Autowired
    private PedidosProductosServicio servicioPedidosProductos;

    @GetMapping("/pedidosProductos")
    public List<PedidosProductos> getPedidosProductos() {
        return servicioPedidosProductos.allPedidos();
    }
    
    @GetMapping("/pedidosProductos/{idPedido}")
    public List<PedidosProductos> getProductos(@PathVariable UUID idPedido) {
        return servicioPedidosProductos.pedidosProducto(idPedido);
    }
    
    @PostMapping("/pedidosProductos/{idPedido}")
    public List<PedidosProductos> postMethodName(@PathVariable UUID idPedido,@RequestBody List<PedidosProductosDTO> productos) {
        
        return servicioPedidosProductos.productosPedidos(productos, idPedido);
    }
    @GetMapping("/cantidadPeidosProductos")
    public List<Object[]> getCantidadPeidosProductos() {
        return servicioPedidosProductos.cantidadPedidosProductos();
    }
    
}
