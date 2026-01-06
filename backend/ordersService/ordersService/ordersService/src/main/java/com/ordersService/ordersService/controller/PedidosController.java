package com.ordersService.ordersService.controller;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ordersService.ordersService.service.PedidosServicio;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import com.ordersService.ordersService.model.Pedidos;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;



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
    System.out.println(idPedido+"mira aca hay un error ");
    Pedidos pedido = servicioPedidos.pedido(idPedido);
    
    if (pedido == null) {
        return ResponseEntity.notFound().build(); 
    }
    
    return ResponseEntity.ok(pedido); 
}

    @PostMapping("/crearPedido")
    public Pedidos postMethodName(@RequestBody Pedidos pedidos) {
        return servicioPedidos.crearPedido(pedidos);
    }
    
    
}
