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
		_, err := services.GetTurboSMTPAuthToken()
		if err != nil {
			fmt.Println("Error de auth en segundo plano:", err)
			return
		}

		codigo := "Pago Realizado, atento para el envio de su pedido"
		err = services.EnviarCodigoVerificacionSMTP(destinatario, codigo)
		if err != nil {
			fmt.Println("Error de envío en segundo plano:", err)
		}
	}(req.Correo)

	c.JSON(http.StatusOK, gin.H{
		"mensaje": "Si el correo está registrado, recibirá un código en breve",
		"estado":  "procesando",
	})
}

func NotificacionEnvio(c *gin.Context) {
	var req EmailRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Formato de correo inválido"})
		return
	}

	go func(destinatario string) {
		_, err := services.GetTurboSMTPAuthToken()
		if err != nil {
			fmt.Println("Error de auth en segundo plano:", err)
			return
		}

		codigo := "Su pedido fue enviado"
		err = services.EnviarCodigoVerificacionSMTP(destinatario, codigo)
		if err != nil {
			fmt.Println("Error de envío en segundo plano:", err)
		}
	}(req.Correo)

	c.JSON(http.StatusOK, gin.H{
		"mensaje": "Si el correo está registrado, recibirá un código en breve",
		"estado":  "procesando",
	})
}
func NotificacionEntregado(c *gin.Context) {
	var req EmailRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Formato de correo inválido"})
		return
	}

	go func(destinatario string) {
		_, err := services.GetTurboSMTPAuthToken()
		if err != nil {
			fmt.Println("Error de auth en segundo plano:", err)
			return
		}

		codigo := "Su pedido ya esta en su destino, por favor retirar"
		err = services.EnviarCodigoVerificacionSMTP(destinatario, codigo)
		if err != nil {
			fmt.Println("Error de envío en segundo plano:", err)
		}
	}(req.Correo)

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
		_, err := services.GetTurboSMTPAuthToken()
		if err != nil {
			fmt.Println("Error de auth en segundo plano:", err)
			return
		}

		codigo := "Pedido Creado"
		err = services.EnviarCodigoVerificacionSMTP(destinatario, codigo)
		if err != nil {
			fmt.Println("Error de envío en segundo plano:", err)
		}
	}(req.Correo)

	c.JSON(http.StatusOK, gin.H{
		"mensaje": "Si el correo está registrado, recibirá un código en breve",
		"estado":  "procesando",
	})
}
