# Plan de Migración — Focus Matafuegos Cloud

## Cronograma de implementación (Gantt)

| Semana | Etapa | Tareas | Estado |
|---|---|---|---|
| Semana 1 | Diseño y contenido | Diseño de la landing page, definición de contenido, arquitectura AWS | ✅ Completado |
| Semana 2 | Infraestructura base | Configuración S3, IAM, bucket policy, static website hosting | ✅ Completado |
| Semana 3 | CDN y dominio | Configuración CloudFront, certificado SSL, Route 53 | ⬜ Pendiente |
| Semana 4 | Formulario y pruebas | Configuración SES, pruebas end-to-end, go-live | ⬜ Pendiente |

## Detalle por etapa

### Etapa 1 — Diseño y contenido (Semana 1)
- Relevamiento del sitio actual
- Diseño de la nueva landing page en HTML/CSS
- Definición de arquitectura AWS (5 servicios)
- Documentación de decisiones técnicas
- Estimación de costos con AWS Pricing Calculator

### Etapa 2 — Infraestructura base (Semana 2)
- Creación del bucket S3 con static website hosting
- Configuración de bucket policy (acceso público de solo lectura)
- Creación del rol IAM con privilegio mínimo para CloudFront
- Deploy de la landing page al bucket S3
- Pruebas de acceso directo a S3

### Etapa 3 — CDN y dominio (Semana 3)
- Creación de la distribución CloudFront
- Configuración de Origin Access Control (OAC)
- Certificado SSL gratuito via AWS Certificate Manager (ACM)
- Configuración de Route 53 — hosted zone y registros A
- Apuntar dominio matafuegosfocus.com.ar a CloudFront
- Pruebas de performance y caché

### Etapa 4 — Formulario y go-live (Semana 4)
- Verificación del dominio en SES
- Salida del sandbox de SES
- Pruebas del formulario de contacto end-to-end
- Monitoreo con CloudWatch (alarma de errores 4xx/5xx)
- Go-live — corte del sitio WordPress al nuevo sitio AWS
- Documentación final

## Pre-requisitos antes del go-live

| Tarea | Cuándo hacerlo | Por qué |
|---|---|---|
| Verificar dominio en SES | Semana 3 | Obligatorio para enviar mails — puede tardar 24-48hs |
| Solicitar salida del sandbox de SES | Semana 3 | Sin esto SES solo manda a mails verificados |
| Revisar landing en móvil y desktop | Semana 4 | Asegurar que se ve bien en todos los dispositivos |
| Elegir horario de corte DNS | Semana 4 | Hacerlo un fin de semana con bajo tráfico |