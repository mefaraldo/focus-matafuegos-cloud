# Focus Matafuegos Cloud
**Proyecto Final — Certificación Cloud Architecture ITBA**

Migración de la landing page de Focus Matafuegos a AWS.
Empresa de mantenimiento y venta de extintores.

---

## ¿Qué hace este proyecto?

Despliega una landing page estática en AWS usando S3, CloudFront, IAM, SES y Route 53.
Todo corre en LocalStack.

## Servicios AWS utilizados

| Servicio | Para qué |

| S3 | Hosting estático de la landing page |
| CloudFront | CDN — distribuye el contenido rápido en todo el país |
| IAM | Roles y permisos con privilegio mínimo |
| SES | Formulario de contacto que envía mails |
| Route 53 | Dominio propio apuntando a CloudFront |

## Cómo correr el proyecto

### Requisitos
- Docker
- Python 3.10+
- AWS CLI

### 1. Clonar el repo
```bash
git clone https://github.com/mefaraldo/focus-matafuegos-cloud
cd focus-matafuegos-cloud
```

### 2. Levantar LocalStack
```bash
docker compose up -d localstack
```

### 3. Configurar credenciales (LocalStack)
```bash
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
alias awslocal="aws --endpoint-url=http://localhost:4566"
```

### 4. Correr el deploy
```bash
python3 scripts/deploy.py
```

### 5. Verificar
```bash
awslocal s3 ls s3://focus-matafuegos-landing
```

La landing page queda disponible en:
`http://localhost:4566/focus-matafuegos-landing/index.html`

## Documentación

| Archivo | Contenido |

| `docs/architecture.md` | Arquitectura y servicios AWS |
| `docs/decisions.md` | Decisiones técnicas justificadas |
| `docs/costs.md` | Estimación de costos ($1.61/mes) |
| `docs/gantt.md` | Cronograma de migración (4 semanas) |
| `app/public/index.html` | Landing page de Matafuegos Focus |
| `scripts/deploy.py` | Script de deploy en LocalStack |

## Costos estimados

Estimación completa: https://calculator.aws/#/estimate?id=9eb88e63750112331733d8e134162b7493020017

**Total: $1.61/mes** ($19.32/año)

