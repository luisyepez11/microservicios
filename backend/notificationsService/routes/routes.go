package routes

import (
	"notificationsService/controllers"

	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	r := gin.Default()
	api := r.Group("/api")
	{
		// --- RUTA DE SALUD ---
		api.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{"message": "pong"})
		})

		authGroup := api.Group("/notificacion")
		{
			authGroup.POST("/pedido", controllers.NotificacionPedido)
			authGroup.POST("/pago", controllers.NotificacionPago)
		}
	}
	return r
}
