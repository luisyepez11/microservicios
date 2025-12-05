#![allow(unused)]
use uuid::Uuid;
use std::{net::SocketAddr, time::Duration};

use axum::{
    Router, extract::{Path, Query, State}, response::{Html, IntoResponse, Json}, routing::{get, get_service, post, put}
};
use serde::{Deserialize, Serialize};
use tower_http::services::ServeDir;
use tower_http::cors::{CorsLayer, Any};
use sqlx::{FromRow, PgPool, pool, postgres::PgPoolOptions, query}; 

#[tokio::main]
async fn main() {
    // 1. Configuración DB
    let database_url = "postgres://postgres:prueba123@db:5432/stock_api";
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .acquire_timeout(Duration::from_secs(10))
        .connect(database_url)
        .await
        .expect("Error conectando a la base de datos");

    // Configuración CORS
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let routes_all = Router::new()
        .merge(routes())     
        .route("/db-check", get(handler_db_check)) 
        .fallback_service(routes_static()) 
        .with_state(pool)
        .layer(cors);  


    let addr = SocketAddr::from(([0,0,0,0], 8003));
    println!("->> LISTENING on http://{addr}\n");
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, routes_all)
        .await
        .unwrap();
}

// --- Modelos ---

#[derive(Debug, Deserialize, Serialize, FromRow)] 
pub struct Stock {
    pub id_stock: Option<Uuid>, 
    pub id_producto: i64,
    pub cantidad: i32,
}

#[derive(Debug, Deserialize)]
struct HelloParams {
    name: Option<String>
}

#[derive(Debug, Deserialize)]  
pub struct HelloData {
    pub name: Option<String>,
}

//metodos get
async fn get_stocks(State(pool): State<PgPool>) -> impl IntoResponse {
    println!("->>{:<12} - get_stocks","HANDLER");

    let stock = sqlx::query_as::<_, Stock>("SELECT * FROM stock") 
        .fetch_all(&pool)
        .await;

    match stock {
        Ok(registro) => Json(registro).into_response(), 
        Err(e) => {
            eprintln!("Error al consultar stock: {}", e);
            (
                axum::http::StatusCode::INTERNAL_SERVER_ERROR,
                format!("Error de base de datos: {}", e),
            ).into_response()
        }
    }
}

async fn get_stock(State(pool): State<PgPool>, Path(id_producto): Path<i64>) -> impl IntoResponse {

    match sqlx::query_as::<_, Stock>(
        "SELECT * FROM stock WHERE id_producto = $1"
    )
    .bind(id_producto)
    .fetch_one(&pool)  
    .await {
        Ok(stocks) => Json(stocks).into_response(),
        Err(e) => {
            eprintln!("Error al consultar stock: {}", e);
            (
                axum::http::StatusCode::INTERNAL_SERVER_ERROR,
                format!("Error de base de datos: {}", e),
            ).into_response()
        }
    }
}

//metodos post
async fn post_stock(State(pool): State<PgPool> ,Json(body): Json<Stock>) -> impl IntoResponse {
    println!("->>{:<12} - post_stock","HANDLER");
    
    let id_producto: i64 = body.id_producto;
    let cantidad: i32 = body.cantidad;
    
    match sqlx::query(
        "INSERT INTO stock (id_producto, cantidad) VALUES ($1, $2)"
    )
    .bind(id_producto)
    .bind(cantidad)
    .execute(&pool)
    .await {
        Ok(result) => {
            println!("Stock insertado correctamente, filas afectadas: {}", result.rows_affected());
            (axum::http::StatusCode::CREATED, "Stock creado exitosamente").into_response()
        },
        Err(e) => {
            eprintln!("Error al insertar stock: {}", e);
            (
                axum::http::StatusCode::INTERNAL_SERVER_ERROR,
                format!("Error al crear stock: {}", e),
            ).into_response()
        }
    }
}

//metodos put
async  fn put_cantidad_stock_aumento(State(pool): State<PgPool>,Json(body): Json<Stock>)  -> impl IntoResponse{
    let id_producto = body.id_producto;
    let cantidad = body.cantidad;
    
    match sqlx::query("UPDATE stock SET cantidad=$1 WHERE id_producto=$2")
        .bind(cantidad)
        .bind(id_producto)
        .execute(&pool)
        .await {
        Ok(result) => {
            println!("Stock modificar correctamente, filas afectadas: {}", result.rows_affected());
            (axum::http::StatusCode::CREATED, "Stock modificar exitosamente").into_response()
        },
        Err(e) => {
            eprintln!("Error al modificar stock: {}", e);
            (
                axum::http::StatusCode::INTERNAL_SERVER_ERROR,
                format!("Error al modificar stock: {}", e),
            ).into_response()
        }
    }
}

async fn handler_db_check(State(pool): State<PgPool>) -> impl IntoResponse {
    let row: (i64,) = sqlx::query_as("SELECT 1")
        .fetch_one(&pool)
        .await
        .unwrap_or((0,));

    Html(format!("Base de datos conectada. Ping: {}", row.0))
}

fn routes_static() -> Router {
    Router::new().fallback_service(ServeDir::new("./"))
}

fn routes() -> Router<PgPool> {
    Router::new()
        /*get */
        .route("/api", get(get_stocks)) 
        .route("/api/{id_producto}", get(get_stock))
        /*put */
        .route("/api", put(put_cantidad_stock_aumento))
        /*post */
        .route("/api", post(post_stock))
}
