import { Pool } from "pg";
import { DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER } from './config.js';

export const pool = new Pool({
  host: DB_HOST,
  user: DB_USER,
  password: DB_PASSWORD,
  port: DB_PORT,
  database: DB_DATABASE,
});

pool.connect()
  .then((client) => {
    console.log("Conexión exitosa a la base de datos PostgreSQL");
    client.release(); 
  })
  .catch((err) => {
    console.error("Error al conectarse a la base de datos PostgreSQL:");

    switch (err.code) {
      case "ECONNREFUSED":
        console.error(`No se pudo conectar al servidor PostgreSQL en ${DB_HOST}:${DB_PORT}.`);
        console.error("Verifica que el servidor PostgreSQL esté en ejecución y que el puerto sea correcto.");
        break;

      case "28P01": 
        console.error(`Error de autenticación: Verifica el usuario (${DB_USER}) y la contraseña.`);
        break;

      case "3D000": 
        console.error(`La base de datos '${DB_DATABASE}' no existe. Verifica el nombre de la base de datos.`);
        break;

      case "ETIMEDOUT":
        console.error(`Tiempo de espera agotado al intentar conectarse a ${DB_HOST}:${DB_PORT}.`);
        console.error("Verifica tu conexión a internet, el firewall y que el servidor PostgreSQL esté accesible.");
        break;

      default:
        console.error("Error desconocido:", err);
        break;
    }
  });


