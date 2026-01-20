package com.ordersService.ordersService.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import com.ordersService.ordersService.model.PedidosProductos;

@Repository
public interface PedidosProductosRepository extends JpaRepository<PedidosProductos,UUID>{

    List<PedidosProductos> findByPedidos_IdPedido(UUID id);

    @Query("SELECT pp.idProducto, COUNT(pp) FROM PedidosProductos pp GROUP BY pp.idProducto")
    List<Object[]> countPedidosByProducto();
}
