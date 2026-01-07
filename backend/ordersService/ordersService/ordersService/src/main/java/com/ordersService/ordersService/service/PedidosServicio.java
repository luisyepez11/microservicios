package com.ordersService.ordersService.service;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ordersService.ordersService.model.Pedidos;
import com.ordersService.ordersService.repository.PedidosProductosRepository;
import com.ordersService.ordersService.repository.PedidosRepository;

import jakarta.transaction.Transactional;

@Service
public class PedidosServicio {
    @Autowired
    private PedidosRepository repositoriopedidos;
    @Transactional
    public List<Pedidos> pedidos(){
        return  repositoriopedidos.findAll();
    }
    @Transactional
    public Pedidos crearPedido(Pedidos pedido){
        Pedidos pd = repositoriopedidos.save(pedido);
        
        return pd;
    }

    @Transactional
    public Pedidos pedido(UUID idPedido){
        return repositoriopedidos.getById(idPedido);
    }

    @Transactional
    public Pedidos pedidoPagado(UUID idPedido){
        Pedidos pedido = pedido(idPedido);
        pedido.setEstado("PAGADO");
        return repositoriopedidos.save(pedido);
    }

}
