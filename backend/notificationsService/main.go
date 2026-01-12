package main

import (
	"log"
	"notificationsService/routes"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error al cargar el archivo .env")
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8090"
	}

	r := routes.SetupRouter()
	r.Run(":" + port)
}
