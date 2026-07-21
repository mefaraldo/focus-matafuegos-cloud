# Decision Log — Focus Matafuegos Cloud

## Formato

Decision:
Contexto:
Alternativas:
Tradeoff:
Resultado:

## Decisiones

### 001 - S3 para hosting estático en lugar de servidor propio

Decision: alojar la landing page en S3 con static website hosting en lugar de un servidor EC2.
Contexto: la landing page es un sitio estático (HTML/CSS/JS) sin lógica de servidor. No necesita una máquina virtual corriendo 24/7.
Alternativas: EC2 con nginx, Vercel, Netlify.
Tradeoff: S3 no puede ejecutar código del lado del servidor (PHP, Python, etc.). Para una landing estática eso no es limitación.
Resultado: S3 reduce el costo a centavos por mes y elimina la operación de un servidor.

### 002 - CloudFront como CDN frente a S3

Decision: usar CloudFront para distribuir el contenido de S3 en lugar de servir S3 directamente.
Contexto: S3 puede servir archivos directamente, pero desde una sola región. CloudFront los distribuye desde edge locations cercanas al usuario.
Alternativas: servir S3 directo, usar otro CDN (Cloudflare).
Tradeoff: CloudFront agrega una capa de configuración. A cambio: HTTPS, dominio propio, caché y mejor performance en Argentina.
Resultado: CloudFront frente a S3 — el bucket queda privado, solo CloudFront puede leerlo.

### 003 - IAM con privilegio mínimo para acceso a S3

Decision: usar un rol IAM con política de solo lectura sobre el bucket, en lugar de hacer el bucket público.
Contexto: un bucket S3 público es un riesgo de seguridad — cualquiera puede listar y descargar los archivos.
Alternativas: bucket público, credenciales hardcodeadas.
Tradeoff: requiere configurar una bucket policy y una OAC (Origin Access Control) en CloudFront.
Resultado: bucket privado + OAC en CloudFront. Solo CloudFront puede leer el contenido.

### 004 - SES para el formulario de contacto

Decision: usar SES para enviar los mails del formulario de contacto en lugar de un servicio externo (Formspree, EmailJS).
Contexto: el formulario necesita enviar un mail a focusmatafuegos@gmail.com cuando alguien completa sus datos.
Alternativas: Formspree (tercero), EmailJS (tercero), SMTP propio.
Tradeoff: SES requiere verificar el dominio y salir del sandbox para envío real. A cambio: costo muy bajo ($0.10 por 1000 mails) y control total.
Resultado: SES con dominio verificado para envío de notificaciones de contacto.

### 005 - Route 53 para el dominio

Decision: usar Route 53 para apuntar el dominio existente a CloudFront.
Contexto: Focus Matafuegos ya tiene un dominio. Hay que apuntarlo a la nueva infraestructura en AWS.
Alternativas: configurar el DNS en el registrador actual (NIC Argentina, etc.).
Tradeoff: Route 53 tiene un costo fijo de $0.50/mes por zona hosted. A cambio: integración nativa con CloudFront y health checks.
Resultado: zona hosted en Route 53 con registro A apuntando a la distribución CloudFront.