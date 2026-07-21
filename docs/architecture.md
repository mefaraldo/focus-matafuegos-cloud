# Arquitectura — Focus Matafuegos Cloud

## Descripción del proyecto

Migración de la landing page de Focus Matafuegos a AWS.
El sitio actual es estático y está desactualizado. 
El nuevo sitio se aloja en S3, se distribuye con CloudFront y 
tiene un formulario de contacto que envía mails via SES.

**Empresa:** Focus Matafuegos — servicio de mantenimiento de extintores, Adrogué, Buenos Aires.
**Usuarios:** clientes potenciales que buscan el servicio online.
**Objetivo:** modernizar la presencia web con una arquitectura cloud profesional, escalable y de bajo costo.

---

## Diagrama de componentes

Internet
    │
    ▼
CloudFront (CDN)
    │  distribuye contenido estático con baja latencia
    ▼
S3 Bucket (hosting estático)
    │  almacena HTML, CSS, JS, imágenes
    │
    ▼
SES (Simple Email Service)
    │  recibe envíos del formulario de contacto
    ▼
Mail del negocio (focusmatafuegos@gmail.com)

IAM → roles y permisos para todo lo anterior
Route 53 → dominio apuntando a CloudFront

---

## Servicios usados

| Servicio | Para qué | Clase del curso |
|---|---|---|
| S3 | Hosting estático de la landing page | 06 |
| CloudFront | CDN — distribuye el contenido rápido en todo el país | 07 |
| IAM | Roles y permisos mínimos para acceder a S3 | 04 |
| SES | Envío de mails desde el formulario de contacto | — |
| Route 53 | Dominio propio apuntando a CloudFront | 07 |

---

## Componentes del stack

| Componente | Servicio AWS | Estado |
|---|---|---|
| Landing page (HTML/CSS/JS) | S3 bucket con static website hosting | por implementar |
| CDN | CloudFront distribution | por implementar |
| Seguridad | IAM + bucket policy | por implementar |
| Formulario de contacto | SES | por implementar |
| Dominio | Route 53 | por implementar |

---

## Decisiones pendientes

- Ver docs/decisions.md