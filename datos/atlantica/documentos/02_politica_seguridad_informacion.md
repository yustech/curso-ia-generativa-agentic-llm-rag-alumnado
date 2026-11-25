---
titulo: Política de seguridad de la información
codigo: ATL-SEG-002
version: 6.1
fecha: 2026-03-01
propietario: Oficina de Seguridad
clasificacion: Interno
---

# Política de seguridad de la información

## 1. Objeto

Esta política establece las reglas mínimas para proteger la información de Atlántica Logística, de sus clientes y de sus empleados. Es de obligado cumplimiento para toda la plantilla, el personal externo y los proveedores con acceso a sistemas de la empresa.

## 2. Clasificación de la información

Toda información tiene una de estas cuatro clasificaciones. Si un documento no indica su clasificación, se trata como **Interno**.

| Nivel | Ejemplos | Puede compartirse con |
| --- | --- | --- |
| Público | Web corporativa, notas de prensa | Cualquiera |
| Interno | Procedimientos, organigramas, este documento | Plantilla y externos con contrato |
| Confidencial | Datos personales de empleados y conductores, contratos y tarifas de clientes, código fuente | Personas autorizadas por el propietario del dato |
| Restringido | Credenciales, claves de cifrado, datos de salud, información de investigaciones internas | Lista nominal aprobada por la Oficina de Seguridad |

## 3. Identidad y acceso

- La autenticación multifactor (MFA) es obligatoria para todos los accesos remotos y para cualquier sistema que contenga información Confidencial o Restringida.
- Las contraseñas tienen al menos 14 caracteres. No se reutilizan las 10 últimas.
- Los accesos se conceden por mínimo privilegio y los responsables de cada sistema los revisan cada trimestre.
- Las cuentas de servicio no pueden usarse para iniciar sesión de forma interactiva.

## 4. Protección de datos

- Toda información Confidencial o Restringida se cifra en reposo con AES-256 y en tránsito con TLS 1.2 o superior.
- Las copias de seguridad de producción se conservan 35 días y se prueba su restauración cada semestre.
- Los registros (logs) de seguridad se conservan **400 días** y no pueden contener contraseñas, tokens ni datos personales completos.
- Los entornos de desarrollo y pruebas no pueden contener datos personales reales: se usan datos sintéticos o anonimizados.

## 5. Secretos

Las credenciales y claves de API se guardan en el gestor de secretos corporativo. Está prohibido guardarlas en el código fuente, en ficheros de configuración versionados, en tickets o en chats. Si una credencial se expone, se revoca de inmediato.

## 6. Incidentes de seguridad

Cualquier persona que detecte o sospeche un incidente lo comunica a `seguridad@atlantica.example` en un plazo máximo de **1 hora**. Si el incidente afecta a datos personales, la Oficina de Seguridad valora la notificación a la autoridad de control en un plazo de 72 horas, como exige el RGPD.

## 7. Proveedores

Ningún proveedor accede a información Confidencial sin contrato que incluya cláusulas de confidencialidad y de tratamiento de datos. Los servicios en la nube deben alojar los datos en el Espacio Económico Europeo.

## 8. Incumplimientos

El incumplimiento de esta política puede dar lugar a medidas disciplinarias y, en su caso, a responsabilidades legales.
