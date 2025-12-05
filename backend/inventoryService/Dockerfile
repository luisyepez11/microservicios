
FROM rust:latest AS builder
WORKDIR /app


COPY Cargo.toml Cargo.lock ./


RUN mkdir src
RUN echo "fn main() {println!(\"stub\")}" > src/main.rs

RUN cargo build --release


COPY src ./src


RUN touch src/main.rs


RUN cargo build --release

FROM debian:bookworm-slim


RUN apt-get update && apt-get install -y libssl3 ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY --from=builder /app/target/release/api ./api


EXPOSE 8003

CMD ["./api"]