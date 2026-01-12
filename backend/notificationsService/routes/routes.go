package routes

import (
	"notificationsService/controllers"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	r := gin.Default()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}))
	api := r.Group("/api")
	{
		api.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{"message": "pong"})
		})

		authGroup := api.Group("/notificacion")
		{
			authGroup.POST("/pedido", controllers.NotificacionPedido)
			authGroup.POST("/pago", controllers.NotificacionPago)
			authGroup.POST("/envio", controllers.NotificacionEnvio)
			authGroup.POST("/entregado", controllers.NotificacionEntregado)

		}
	}
	return r
}
