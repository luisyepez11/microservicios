package controllers

import (
	"fmt"
	"net/http"
	"notificationsService/services"

	"github.com/gin-gonic/gin"
)

type EmailRequest struct {
	Correo string `json:"correo" binding:"required,email"`
}

func NotificacionPago(c *gin.Context) {
	var req EmailRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Formato de correo inválido"})
		return
	}

	go func(destinatario string) {
		// Aseguramos el token de TurboSMTP
		_, err := services.GetTurboSMTPAuthToken()
		if err != nil {
			fmt.Println("Error de auth en segundo plano:", err)
			return
		}

		// Enviamos el código (puedes generar uno aleatorio aquí)
		codigo := "Creacion de pedido"
		err = services.EnviarCodigoVerificacionSMTP(destinatario, codigo)
		if err != nil {
			fmt.Println("Error de envío en segundo plano:", err)
		}
	}(req.Correo)

	// 3. Respondemos al cliente de inmediato
	c.JSON(http.StatusOK, gin.H{
		"mensaje": "Si el correo está registrado, recibirá un código en breve",
		"estado":  "procesando",
	})
}

func NotificacionPedido(c *gin.Context) {
	var req EmailRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Formato de correo inválido"})
		return
	}

	go func(destinatario string) {
		// Aseguramos el token de TurboSMTP
		_, err := services.GetTurboSMTPAuthToken()
		if err != nil {
			fmt.Println("Error de auth en segundo plano:", err)
			return
		}

		// Enviamos el código (puedes generar uno aleatorio aquí)
		codigo := "Pago efectuado"
		err = services.EnviarCodigoVerificacionSMTP(destinatario, codigo)
		if err != nil {
			fmt.Println("Error de envío en segundo plano:", err)
		}
	}(req.Correo)

	// 3. Respondemos al cliente de inmediato
	c.JSON(http.StatusOK, gin.H{
		"mensaje": "Si el correo está registrado, recibirá un código en breve",
		"estado":  "procesando",
	})
}
