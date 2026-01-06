package com.ordersService.ordersService.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;
import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
@Entity
@Table(name = "pedidosProductos")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
@Data
public class PedidosProductos {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(updatable=false,nullable=false)
    private UUID idPedidosProductos;

    @ManyToOne
    @JoinColumn(name= "idPedido",nullable = false)
    private Pedidos pedidos;

    @Column(nullable=false)
    private int  idProducto;

    @Column(nullable=false)
    private int cantidadProducto;

    public void setPedidos(Pedidos pedidos) {
    this.pedidos = pedidos;
}

public Pedidos getPedidos() {
    return this.pedidos;
}

public void setIdProducto(int idProducto) {
    this.idProducto = idProducto;
}

public int getIdProducto() {
    return this.idProducto;
}

public void setCantidadProducto(int cantidadProducto) {
    this.cantidadProducto = cantidadProducto;
}

public int getCantidadProducto() {
    return this.cantidadProducto;
}
}
