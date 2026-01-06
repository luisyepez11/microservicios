package com.ordersService.ordersService.model;
import jakarta.persistence.*;
import lombok.Data; 
import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Entity
@Table(name = "pedidos")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
@Data
public class Pedidos {
    @Id
    @GeneratedValue(strategy= GenerationType.UUID)
    @Column(updatable= false,nullable = false)
    private UUID idPedido;

    @Column(nullable=false)
    private UUID idUsuariPedido;

    @Column(nullable=false)
    private String  estado = "CREADO";
    
}
