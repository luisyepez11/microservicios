package main

import (
	"log"
	"notificationsService/routes"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	// 1. Cargar el archivo .env
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error al cargar el archivo .env")
	}

	// 2. Ahora puedes acceder a ellas en cualquier parte
	port := os.Getenv("PORT")
	if port == "" {
		port = "8090"
	}

	r := routes.SetupRouter()
	r.Run(":" + port)
}
