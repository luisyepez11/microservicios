package com.ordersService.ordersService.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity // Forzamos a que esta sea la configuración activa
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable()) // Desactiva la protección de tokens
            .authorizeHttpRequests(auth -> auth
                .anyRequest().permitAll() // Permite TODO sin contraseña
            )
            .headers(headers -> headers.frameOptions(frame -> frame.disable())); // Útil si usas consola H2
        
        return http.build();
    }
}