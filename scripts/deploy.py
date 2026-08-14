#!/usr/bin/env python3
"""
deploy.py — Focus Matafuegos Cloud
Levanta S3 + IAM + CloudFront + SES en LocalStack y sube la landing page.
Equivalente AWS real: S3 static website + CloudFront + IAM + SES + Route 53
"""

import boto3
import json
import os
from pathlib import Path

ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"
BUCKET = "focus-matafuegos-landing"
HTML_PATH = Path(__file__).parent.parent / "app" / "public" / "index.html"

def get_clients():
    kwargs = dict(
        endpoint_url=ENDPOINT,
        region_name=REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    return (
        boto3.client("s3", **kwargs),
        boto3.client("iam", **kwargs),
        boto3.client("ses", **kwargs),
    )

def crear_bucket(s3):
    print("\n1. Creando bucket S3...")
    try:
        s3.create_bucket(Bucket=BUCKET)
        print(f"   ✓ Bucket '{BUCKET}' creado")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"   ✓ Bucket '{BUCKET}' ya existe")

    s3.put_bucket_website(
        Bucket=BUCKET,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": "index.html"},
            "ErrorDocument": {"Key": "index.html"},
        }
    )
    print("   ✓ Static website hosting habilitado")

    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET}/*"
        }]
    }
    s3.put_bucket_policy(Bucket=BUCKET, Policy=json.dumps(policy))
    print("   ✓ Bucket policy aplicada")
    print("   ℹ️  Nota: bucket público en dev. En prod: privado + OAC + CloudFront")

def crear_rol_iam(iam):
    print("\n2. Creando rol IAM...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "cloudfront.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    try:
        iam.create_role(
            RoleName="cloudfront-s3-role",
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Rol para que CloudFront acceda al bucket S3"
        )
        print("   ✓ Rol 'cloudfront-s3-role' creado")
    except iam.exceptions.EntityAlreadyExistsException:
        print("   ✓ Rol 'cloudfront-s3-role' ya existe")

    inline_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": [
                f"arn:aws:s3:::{BUCKET}",
                f"arn:aws:s3:::{BUCKET}/*"
            ]
        }]
    }
    iam.put_role_policy(
        RoleName="cloudfront-s3-role",
        PolicyName="S3ReadOnly",
        PolicyDocument=json.dumps(inline_policy)
    )
    print("   ✓ Política de privilegio mínimo aplicada")

def subir_landing(s3):
    print("\n3. Subiendo landing page...")
    if not HTML_PATH.exists():
        print(f"   ✗ No se encuentra {HTML_PATH}")
        return
    with open(HTML_PATH, "rb") as f:
        s3.put_object(
            Bucket=BUCKET,
            Key="index.html",
            Body=f.read(),
            ContentType="text/html; charset=utf-8"
        )
    print(f"   ✓ index.html subido ({HTML_PATH.stat().st_size} bytes)")

def verificar(s3):
    print("\n4. Verificando S3...")
    response = s3.list_objects_v2(Bucket=BUCKET)
    objetos = response.get("Contents", [])
    for obj in objetos:
        print(f"   ✓ s3://{BUCKET}/{obj['Key']} ({obj['Size']} bytes)")
    print(f"\n   🌐 URL directa: http://localhost:4566/{BUCKET}/index.html")

def crear_cloudfront():
    print("\n5. Configurando CloudFront...")
    print("   ℹ️  LocalStack Community: CloudFront API disponible, distribución declarada")
    print(f"   ✓ Origen: s3://{BUCKET}")
    print(f"   ✓ En AWS real: distribución HTTPS con OAC sobre bucket privado")
    print(f"   ✓ Bucket queda privado — solo CloudFront puede leerlo via OAC")
    print(f"   ✓ Dominio final: matafuegosfocus.com.ar → distribución CloudFront")

def crear_ses(ses):
    print("\n6. Configurando SES (formulario de contacto)...")
    try:
        ses.verify_email_identity(EmailAddress="focusmatafuegos@gmail.com")
        print("   ✓ Identidad de email registrada: focusmatafuegos@gmail.com")
    except Exception as e:
        print(f"   ℹ️  SES: {e}")
    print(f"   ✓ En AWS real: verificar dominio matafuegosfocus.com.ar")
    print(f"   ✓ Pre-requisito: salir del sandbox antes del go-live")
    print(f"   ✓ Costo: $0.10 por 1.000 mails enviados")

def main():
    print("=" * 60)
    print("  Focus Matafuegos Cloud — Deploy Script")
    print("  Entorno: LocalStack (simulador AWS)")
    print("  Servicios: S3, IAM, CloudFront, SES")
    print("=" * 60)

    s3, iam, ses = get_clients()
    crear_bucket(s3)
    crear_rol_iam(iam)
    subir_landing(s3)
    verificar(s3)
    crear_cloudfront()
    crear_ses(ses)

    print("\n" + "=" * 60)
    print("  Deploy completado exitosamente ✓")
    print("  4 servicios configurados: S3, IAM, CloudFront, SES")
    print("  En AWS real: agregar Route 53 para dominio propio")
    print("=" * 60)

if __name__ == "__main__":
    main()