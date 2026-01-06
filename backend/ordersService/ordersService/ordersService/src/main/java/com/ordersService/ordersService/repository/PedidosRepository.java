package com.ordersService.ordersService.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.ordersService.ordersService.model.Pedidos;
import com.ordersService.ordersService.model.PedidosProductos;

@Repository
public interface PedidosRepository extends  JpaRepository<Pedidos, UUID>{


}
