---
titulo: Catálogo de módulos de Terraform aprobados
codigo: ATL-INF-007
version: 2026.11
fecha: 2026-11-02
propietario: Plataforma e infraestructura
clasificacion: Interno
---

# Catálogo de módulos de Terraform aprobados

Los módulos se referencian siempre con una versión fija:

```hcl
source = "git::https://git.atlantica.example/infra/modulos.git//<modulo>?ref=v<version>"
```

Los costes son estimaciones mensuales orientativas en la región eu-south-2.

## red_base · v2.3.0

Red del proyecto: VPC, dos subredes privadas, dos subredes públicas y puerta NAT.

| Variable | Tipo | Obligatoria | Descripción |
| --- | --- | --- | --- |
| `proyecto` | string | Sí | Nombre corto del proyecto |
| `entorno` | string | Sí | `dev`, `pre` o `pro` |
| `cidr` | string | No | Por defecto `10.20.0.0/16` |

Coste estimado: 35 € al mes (puerta NAT).

## vm_linux · v1.8.1

Máquina virtual Linux (Ubuntu 24.04) en subred privada, con disco cifrado y agente de monitorización.

| Variable | Tipo | Obligatoria | Descripción |
| --- | --- | --- | --- |
| `nombre` | string | Sí | Sigue la convención `atl-<proyecto>-<entorno>-<recurso>` |
| `tipo_instancia` | string | Sí | Uno de los tipos permitidos por la política |
| `subred_id` | string | Sí | Salida `subredes_privadas` de `red_base` |
| `disco_gb` | number | No | Por defecto 50 |

Coste estimado por máquina: `t3.micro` 9 €, `t3.small` 18 €, `t3.medium` 36 €, `m6i.large` 85 €, `m6i.xlarge` 170 €.

## postgres_gestionado · v3.1.0

PostgreSQL 16 gestionado, cifrado y en subred privada.

| Variable | Tipo | Obligatoria | Descripción |
| --- | --- | --- | --- |
| `nombre` | string | Sí | Nombre de la instancia |
| `clase` | string | Sí | `db.t3.medium` en dev y pre; `db.m6i.large` en pro |
| `multi_az` | bool | Sí | Debe ser `true` en pro |
| `dias_copia` | number | Sí | 7 en dev y pre; 30 en pro |
| `subredes` | list(string) | Sí | Subredes privadas |

Coste estimado: `db.t3.medium` 70 €; `db.m6i.large` Multi-AZ 390 €.

## bucket_privado · v1.4.2

Bucket S3 privado, cifrado, con versionado y bloqueo de acceso público activado (no se puede desactivar).

| Variable | Tipo | Obligatoria | Descripción |
| --- | --- | --- | --- |
| `nombre` | string | Sí | Nombre del bucket |
| `dias_retencion` | number | No | Días antes de mover a almacenamiento frío; por defecto 90 |

Coste estimado: 5 € por cada 100 GB.

## balanceador · v2.0.3

Balanceador de aplicaciones con certificado TLS gestionado. Es el único recurso que puede ir en subred pública.

Coste estimado: 25 €.

## cluster_k8s · v4.0.0

Clúster de Kubernetes gestionado con un grupo de nodos.

| Variable | Tipo | Obligatoria | Descripción |
| --- | --- | --- | --- |
| `nombre` | string | Sí | Nombre del clúster |
| `nodos` | number | Sí | Entre 2 y 10 |
| `tipo_nodo` | string | Sí | `m6i.large` o `m6i.xlarge` |

Coste estimado: 75 € del plano de control más el coste de cada nodo.

## Etiquetas

Todos los módulos aceptan la variable `etiquetas` (map(string)), donde deben ir las cuatro etiquetas obligatorias de la política ATL-INF-006: `proyecto`, `entorno`, `centro_coste` y `responsable`.
