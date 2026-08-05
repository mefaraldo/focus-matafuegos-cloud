# Estimación de Costos — Focus Matafuegos Cloud

## Herramienta: AWS Pricing Calculator
Estimación completa: https://calculator.aws/#/estimate?id=9eb88e63750112331733d8e134162b7493020017

## Stack: Landing page estática en AWS

| Servicio | Configuración | Costo mensual |
|---|---|---|
| S3 Standard | 1 GB almacenamiento + 100 PUT + 10.000 GET requests/mes | $0.03 |
| CloudFront | 5 GB transferencia Sudamérica + 10.000 requests HTTPS/mes | $0.58 |
| Route 53 | 1 hosted zone + 1M consultas estándar/mes | $0.90 |
| SES | 1.000 emails enviados/mes (formulario de contacto) | $0.10 |
| IAM | Roles y políticas (sin costo adicional) | $0.00 |
| **TOTAL** | | **$1.61/mes** |

**Costo anual estimado: $19.32/año**

## Por qué es tan barato

El sitio es estático — sin EC2, sin RDS, sin NAT Gateway.
La arquitectura correcta para una landing page elimina los servicios más caros de AWS.
CloudFront tiene nivel gratuito de 1 TB/mes — con el tráfico de un negocio local el costo real puede ser $0.

## Free tier AWS (primer año)

Con el free tier el primer año el costo sería prácticamente $0:
- S3: 5 GB + 20k GET requests/mes gratis
- CloudFront: 1 TB transferencia + 10M requests/mes gratis
- SES: 3.000 mensajes/mes gratis