package services

import (
	"crypto/tls"
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/go-resty/resty/v2"
	"gopkg.in/gomail.v2"
)

// Variables globales para el caché (equivalente a tus variables globales en Python)
var (
	tokenCache  string
	tokenExpiry time.Time
	mutex       sync.Mutex
	client      = resty.New()
)

func GetTurboSMTPAuthToken() (string, error) {
	mutex.Lock()
	defer mutex.Unlock()

	// 1. Verificar si el token en caché aún es válido
	if tokenCache != "" && time.Now().Before(tokenExpiry) {
		return tokenCache, nil
	}

	// 2. Si no es válido, pedir uno nuevo (Authenticate)
	authData := map[string]string{
		"email":     os.Getenv("TURBOSMTP_EMAIL"),
		"password":  os.Getenv("TURBOSMTP_PASSWORD"),
		"no_expire": "1",
	}

	var result struct {
		Auth string `json:"auth"`
	}

	resp, err := client.R().
		SetHeader("Content-Type", "application/json").
		SetBody(authData).
		SetResult(&result).
		Post("https://dashboard.serversmtp.com/api/authorize")

	if err != nil || resp.IsError() {
		return "", fmt.Errorf("fallo auth turboSMTP: %v", err)
	}

	if result.Auth != "" {
		tokenCache = result.Auth
		tokenExpiry = time.Now().Add(50 * time.Minute) // Caché por 50 min
		fmt.Println("turboSMTP authentication successful (Go)")
		return tokenCache, nil
	}

	return "", fmt.Errorf("auth response missing token")
}

func EnviarCodigoVerificacionSMTP(destinatario string, transaccion string) error {

	server := "pro.turbo-smtp.com"
	port := 465
	user := os.Getenv("TURBOSMTP_CONSUMER_KEY")
	pass := os.Getenv("TURBOSMTP_CONSUMER_SECRET")
	from := os.Getenv("TURBOSMTP_FROM_EMAIL")

	m := gomail.NewMessage()
	m.SetHeader("From", from)
	m.SetHeader("To", destinatario)
	m.SetHeader("Subject", "Código de Verificación - Sistema Go")

	htmlBody := fmt.Sprintf(`
		<html>
		<body>
			<h2>Notificacion de transacción</h2>
			<p>Transacción realizada : <strong>%s</strong></p>
			<p>Si no solicitaste este código, ignora este mensaje.</p>
		</body>
		</html>`, transaccion)

	m.SetBody("text/html", htmlBody)

	d := gomail.NewDialer(server, port, user, pass)
	d.TLSConfig = &tls.Config{InsecureSkipVerify: false, ServerName: server}

	// Enviar
	if err := d.DialAndSend(m); err != nil {
		return fmt.Errorf("error SMTP: %v", err)
	}

	fmt.Printf("Correo enviado exitosamente a %s vía SMTP (Go)\n", destinatario)
	return nil
}
