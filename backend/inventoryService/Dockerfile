# Fase de construcción
FROM rust:latest AS builder
WORKDIR /app

# --- MEJORAS DE RED Y RENDIMIENTO ---
# Usar el protocolo 'sparse' es mucho más rápido y ligero para descargar dependencias
ENV CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse
# Aumentar el tiempo de espera a 2 minutos para conexiones lentas
ENV CARGO_HTTP_TIMEOUT=120
# Forzar a cargo a reintentar descargas fallidas
ENV CARGO_NET_RETRY=5
# ------------------------------------

# Copiar archivos de dependencias
COPY Cargo.toml Cargo.lock ./

# Crear un proyecto vacío para cachear las dependencias
RUN mkdir src
RUN echo "fn main() {println!(\"stub\")}" > src/main.rs

# Primera compilación: descarga y compila solo las librerías
RUN cargo build --release

# Ahora copiar el código real de tu aplicación
COPY src ./src

# Actualizar la fecha de modificación para que Cargo sepa que debe recompilar el binario
RUN touch src/main.rs

# Segunda compilación: compila tu código real
RUN cargo build --release

# Fase final: Imagen ligera para ejecución
FROM debian:bookworm-slim

# Instalar librerías necesarias para el binario de Rust y certificados para HTTPS
RUN apt-get update && apt-get install -y \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el binario generado en la fase anterior
COPY --from=builder /app/target/release/api ./api

# Exponer el puerto configurado en main.rs
EXPOSE 8003

# Ejecutar la aplicación
CMD ["./api"]