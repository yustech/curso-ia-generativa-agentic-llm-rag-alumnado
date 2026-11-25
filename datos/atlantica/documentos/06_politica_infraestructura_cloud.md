---
titulo: Política de infraestructura en la nube
codigo: ATL-INF-006
version: 5.0
fecha: 2026-06-10
propietario: Plataforma e infraestructura
clasificacion: Interno
---

# Política de infraestructura en la nube

## 1. Alcance

Se aplica a todos los recursos que Atlántica Logística despliega en su proveedor de nube pública (AWS). Toda la infraestructura se define como código con **Terraform** usando los módulos del catálogo aprobado (ATL-INF-007). No se crean recursos a mano desde la consola, salvo en emergencias registradas.

## 2. Regiones

- Región principal: **eu-south-2 (España)**.
- Región de recuperación ante desastres: **eu-west-1 (Irlanda)**, solo para copias y réplicas de producción.
- Está prohibido desplegar en regiones fuera de la Unión Europea.

## 3. Entornos y nombres

Existen tres entornos: `dev` (desarrollo), `pre` (preproducción) y `pro` (producción).

Los recursos se nombran así: `atl-<proyecto>-<entorno>-<recurso>`, todo en minúsculas y con guiones. Ejemplo: `atl-faro-pre-db`.

## 4. Etiquetas obligatorias

Todo recurso lleva estas cuatro etiquetas. Un recurso sin ellas se considera no conforme y se elimina en la revisión semanal:

| Etiqueta | Valores |
| --- | --- |
| `proyecto` | Nombre corto del proyecto (por ejemplo, `faro`) |
| `entorno` | `dev`, `pre` o `pro` |
| `centro_coste` | Código de 4 cifras del centro de coste (por ejemplo, `4120`) |
| `responsable` | Correo de la persona responsable |

## 5. Cómputo

Tipos de instancia permitidos: `t3.micro`, `t3.small`, `t3.medium`, `m6i.large` y `m6i.xlarge`. Cualquier otro tipo (incluidas las instancias con GPU) necesita aprobación de la Oficina de Arquitectura.

## 6. Bases de datos

- Motor estándar: PostgreSQL 16 gestionado (módulo `postgres_gestionado`).
- En `dev` y `pre` se usa la clase `db.t3.medium` y las copias se conservan **7 días**.
- En `pro` la base de datos es **Multi-AZ** obligatoriamente y las copias se conservan **30 días**.

## 7. Almacenamiento y red

- Todos los buckets son privados y cifrados. **Está prohibido cualquier bucket con acceso público.**
- Los volúmenes y las bases de datos se cifran en reposo.
- Las bases de datos y los servidores de aplicación van en subredes privadas. Solo los balanceadores pueden estar en subredes públicas.
- No se abren puertos de administración (22, 3389) a Internet.

## 8. Costes

| Entorno | Coste mensual estimado que puede aprobar el responsable del proyecto |
| --- | --- |
| `dev` | Hasta 300 € |
| `pre` | Hasta 800 € |
| `pro` | Siempre pasa por el Comité de Cambios (CAB) |

Por encima de esos importes, la petición requiere la aprobación de la dirección de Sistemas.

## 9. Cambios

Todo despliegue en `pro` sigue el Procedimiento de gestión de cambios (ATL-OPS-008). Los cambios en `dev` y `pre` se aplican desde el pipeline tras la revisión del plan de Terraform por otra persona del equipo.
