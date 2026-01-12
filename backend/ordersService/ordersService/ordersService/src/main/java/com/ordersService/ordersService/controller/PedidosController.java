package com.ordersService.ordersService.controller;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.ordersService.ordersService.model.Pedidos;
import com.ordersService.ordersService.service.PedidosServicio;

import jakarta.websocket.server.PathParam;

import org.springframework.web.bind.annotation.RequestParam;





@RestController
public class PedidosController {

    @Autowired
    private PedidosServicio servicioPedidos;

    @GetMapping("/")
    public List<Pedidos> getPedidos() {
        return servicioPedidos.pedidos();
    }

@GetMapping("/{idPedido}")
public ResponseEntity<Pedidos> getPedidos(@PathVariable UUID idPedido) {
    Pedidos pedido = servicioPedidos.pedido(idPedido);
    
    if (pedido == null) {
        return ResponseEntity.notFound().build(); 
    }
    
    return ResponseEntity.ok(pedido); 
}

    @PostMapping("/crearPedido")
    public Pedidos crearPedido(@RequestBody Pedidos pedidos) {
        return servicioPedidos.crearPedido(pedidos);
    }
    @PutMapping("/pagarPedido/{idPedido}")
    public Pedidos pagarPedido(@PathVariable UUID idPedido) {
        return servicioPedidos.pedidoPagado(idPedido);
    }
    @PutMapping("/entregarPedido/{idPedido}")
    public Pedidos entregarPedido(@PathVariable UUID idPedido) {
        return servicioPedidos.pedidoEntregado(idPedido);
    }
    
    @GetMapping("/pedidosUsuarios/{idUsuariPedido}")
    public List<Pedidos> pedidosUsuarios(@PathVariable UUID idUsuariPedido) {
        return servicioPedidos.pedidosUsuarios(idUsuariPedido);
    }
    
    
}
