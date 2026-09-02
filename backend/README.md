# SISTEMA SIHS — Backend API

Backend del **Sistema de Información SIHS**, construido con **FastAPI**, **SQLAlchemy**, **PostgreSQL** y autenticación mediante **JWT**.

El proyecto sigue una arquitectura por capas, buscando mantener separadas las responsabilidades entre rutas, controladores, servicios, repositorios, modelos y esquemas.

---

## Estado actual

### Autenticación y autorización

* [x] Registro público de usuarios
* [x] Hash de contraseñas con Argon2
* [x] Login mediante email y contraseña
* [x] Generación de JWT
* [x] Validación de firma JWT
* [x] Validación de expiración
* [x] Validación del algoritmo JWT
* [x] Validación del `sub`
* [x] Validación de UUID del usuario
* [x] Validación de usuario activo
* [x] Autenticación mediante Bearer Token
* [x] Autorización por roles
* [x] Rol `USER`
* [x] Rol `ADMIN`
* [x] Protección de endpoints administrativos
* [x] Desactivación lógica de usuarios
* [x] Activación de usuarios
* [x] Protección contra modificación del rol mediante actualización pública

### Pruebas

La suite actual cuenta con:

**103 tests pasando.**

```text
103 passed
```

Las pruebas cubren principalmente:

* Registro
* Usuarios
* Roles
* Autenticación
* JWT
* Autorización
* Usuarios activos/inactivos
* Permisos administrativos
* Casos de tokens inválidos
* Expiración de tokens
* Algoritmos JWT
* Integridad del `sub`
* Acceso a `/users/me`

---

# Tecnologías

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Pydantic Settings

## Seguridad

* PyJWT
* Argon2

## Testing

* pytest
* FastAPI `TestClient`

## Base de datos

* PostgreSQL
* SQLAlchemy ORM
* Psycopg

---

# Arquitectura

El proyecto utiliza una arquitectura por capas:

```text
HTTP Request
     │
     ▼
   Routes
     │
     ▼
 Controllers
     │
     ▼
  Services
     │
     ▼
 Repositories
     │
     ▼
 SQLAlchemy Models
     │
     ▼
 PostgreSQL
```

Las responsabilidades principales son:

### Routes

Responsables de:

* Definir endpoints.
* Recibir requests.
* Declarar dependencias.
* Definir response models.
* Delegar la operación al controller.

Las rutas no deben contener lógica de negocio compleja.

---

### Controllers

Responsables de:

* Coordinar la operación.
* Recibir schemas.
* Invocar servicios.
* Transformar resultados al schema correspondiente.

---

### Services

Contienen la lógica de negocio.

Por ejemplo, el proceso de autenticación:

```text
email + password
       │
       ▼
buscar usuario
       │
       ├── no existe ──────► 401
       │
       ▼
verificar password
       │
       ├── incorrecta ─────► 401
       │
       ▼
verificar usuario activo
       │
       ├── inactivo ───────► 401
       │
       ▼
crear JWT
       │
       ▼
access_token
```

---

### Repositories

Responsables de acceder a la base de datos.

Ejemplo:

```text
AuthService
     │
     ▼
UserRepository
     │
     ▼
PostgreSQL
```

Esto permite evitar que los servicios tengan consultas SQL/ORM directamente mezcladas con la lógica de negocio.

---

### Models

Representan las entidades persistidas en PostgreSQL mediante SQLAlchemy.

Actualmente la entidad principal implementada es:

```text
User
```

---

### Schemas

Definen:

* Requests.
* Responses.
* Validación de datos.
* Contratos de la API.

---

# Estructura actual

La estructura principal del proyecto sigue aproximadamente este esquema:

```text
backend/
│
├── app/
│   ├── common/
│   │   └── responses.py
│   │
│   ├── controllers/
│   │   └── auth_controller.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── roles.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   └── user_repository.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   └── user.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── integration/
│   │   └── routes/
│   │       ├── test_auth_routes.py
│   │       └── test_user_routes.py
│   │
│   └── conftest.py
│
├── .env
├── requirements.txt
└── README.md
```

> La estructura puede crecer conforme se incorporen nuevos módulos funcionales al SIHS.

---

# Configuración

La aplicación utiliza variables de entorno mediante `pydantic-settings`.

Configuración actual:

```python
class Settings(BaseSettings):
    app_name: str = "Sistema de Información API"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 5
```

---

# Variables de entorno

Crear un archivo `.env` dentro de `backend/`.

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/sihs

JWT_SECRET_KEY=una-clave-secreta-segura
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=5
```

### Importante

El `.env` no debe subirse al repositorio.

Agregar:

```text
.env
```

al `.gitignore`.

En producción, `JWT_SECRET_KEY` debe utilizar una clave fuerte y generada de forma segura.

---

# Base de datos

La aplicación utiliza PostgreSQL.

La URL se configura mediante:

```env
DATABASE_URL=...
```

Para las pruebas de integración se utiliza una base de datos independiente.

Actualmente la configuración de testing utiliza:

```text
postgresql+psycopg://postgres:admin@localhost:5433/sihs_test
```

o el valor definido en:

```env
TEST_DATABASE_URL
```

---

# Instalación

## 1. Crear entorno virtual

Desde `backend`:

```powershell
python -m venv .venv
```

---

## 2. Activar entorno virtual

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

## 4. Configurar `.env`

Crear:

```text
backend/.env
```

con las variables necesarias.

---

# Ejecutar la aplicación

Desde el directorio `backend`:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible normalmente en:

```text
http://127.0.0.1:8000
```

---

# Documentación de la API

FastAPI proporciona automáticamente:

```text
/docs
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

También está disponible:

```text
/redoc
```

---

# Versionado de API

Actualmente los endpoints utilizan:

```text
/api/v1
```

Esto permite mantener compatibilidad futura si se desarrolla una nueva versión de la API.

---

# Usuarios

## Registro

Endpoint:

```http
POST /api/v1/users
```

El registro es público.

Ejemplo:

```json
{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "3001234567",
    "document_number": "DOC-001",
    "password": "Password123!"
}
```

El usuario registrado recibe automáticamente:

```text
USER
```

El cliente no puede especificar el rol durante el registro.

Esto evita que alguien pueda crear directamente un usuario administrador enviando:

```json
{
    "role": "ADMIN"
}
```

---

# Roles

Actualmente existen:

```text
USER
ADMIN
```

## USER

Un usuario normal puede:

* Autenticarse.
* Consultar su propio perfil.
* Utilizar los endpoints que posteriormente se definan para usuarios normales.

No puede:

* Listar todos los usuarios.
* Consultar otros usuarios.
* Activar usuarios.
* Desactivar usuarios.
* Modificar usuarios administrativamente.

---

## ADMIN

Un administrador puede acceder a las operaciones administrativas de usuarios.

Actualmente puede:

* Listar usuarios.
* Listar usuarios inactivos.
* Consultar un usuario específico.
* Activar usuarios.
* Actualizar usuarios.
* Desactivar usuarios.

---

# Autenticación

## Login

Endpoint:

```http
POST /api/v1/auth/login
```

Request:

```json
{
    "email": "juan@example.com",
    "password": "Password123!"
}
```

Response:

```json
{
    "data": {
        "access_token": "...",
        "token_type": "bearer"
    }
}
```

---

# JWT

Los tokens utilizan actualmente:

```text
Algorithm: HS256
```

El token contiene:

```json
{
    "sub": "UUID_DEL_USUARIO",
    "exp": "FECHA_DE_EXPIRACION"
}
```

## `sub`

Contiene el UUID del usuario autenticado.

Ejemplo:

```text
sub = 8d7c...
```

## `exp`

Define la fecha de expiración del token.

Actualmente:

```text
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=5
```

---

# Validación del JWT

Los tokens son validados mediante:

```python
jwt.decode(
    token,
    settings.jwt_secret_key,
    algorithms=[settings.jwt_algorithm],
)
```

Esto garantiza que el algoritmo aceptado sea explícitamente el configurado.

Se rechazan:

* Tokens expirados.
* Tokens con firma inválida.
* Tokens malformados.
* Tokens con algoritmo incorrecto.
* Tokens con algoritmo `none`.
* Tokens sin `sub`.
* Tokens con `sub` que no sea un UUID válido.
* Tokens correspondientes a usuarios inexistentes.
* Tokens correspondientes a usuarios inactivos.

---

# Bearer Authentication

Los endpoints protegidos utilizan:

```http
Authorization: Bearer <access_token>
```

FastAPI obtiene el token mediante `HTTPBearer`.

El flujo es:

```text
Authorization Header
        │
        ▼
    HTTPBearer
        │
        ▼
  JWT validation
        │
        ▼
   UUID validation
        │
        ▼
 Find active user
        │
        ▼
 Current User
```

---

# Dependencias de autenticación

La aplicación utiliza:

```python
get_current_user
```

para obtener el usuario autenticado.

Y:

```python
get_current_admin
```

para proteger endpoints administrativos.

La diferencia conceptual es:

```text
get_current_user
        ↓
¿Token válido?
        ↓
¿Usuario existe y está activo?
        ↓
Usuario autenticado
```

Mientras que:

```text
get_current_admin
        ↓
get_current_user
        ↓
¿role == ADMIN?
        ↓
Administrador autorizado
```

---

# Códigos HTTP de seguridad

La aplicación diferencia correctamente entre:

### `401 Unauthorized`

Se utiliza cuando la identidad no puede ser autenticada.

Ejemplos:

* No hay token.
* Token inválido.
* Token expirado.
* Firma incorrecta.
* Usuario inexistente.
* Usuario inactivo.
* Credenciales incorrectas.

---

### `403 Forbidden`

Se utiliza cuando el usuario está autenticado pero no tiene permisos suficientes.

Ejemplo:

```text
USER → endpoint ADMIN
```

Resultado:

```http
403 Forbidden
```

Mensaje:

```text
Permisos insuficientes.
```

---

# Endpoints actuales

## Públicos

### Registro

```http
POST /api/v1/users
```

### Login

```http
POST /api/v1/auth/login
```

---

## Usuario autenticado

### Mi perfil

```http
GET /api/v1/users/me
```

Requiere:

```http
Authorization: Bearer <token>
```

Disponible para:

```text
USER
ADMIN
```

---

## Administración de usuarios

Requieren rol:

```text
ADMIN
```

### Listar usuarios

```http
GET /api/v1/users
```

### Listar usuarios inactivos

```http
GET /api/v1/users/inactive
```

### Consultar usuario

```http
GET /api/v1/users/{user_uuid}
```

### Activar usuario

```http
PATCH /api/v1/users/{user_uuid}/activate
```

### Actualizar usuario

```http
PUT /api/v1/users/{user_uuid}
```

### Desactivar usuario

```http
DELETE /api/v1/users/{user_uuid}
```

---

# Desactivación de usuarios

La eliminación de usuarios es **lógica**, no física.

Cuando un administrador elimina/desactiva un usuario:

```text
is_active = False
```

El registro permanece en PostgreSQL.

Esto permite conservar la información y evitar la eliminación física de registros relacionados.

Un usuario inactivo:

* No puede iniciar sesión.
* No puede utilizar un token previamente generado.
* No puede acceder a endpoints protegidos.
* Puede ser reactivado por un administrador.

---

# Seguridad del rol

El rol no forma parte de:

```text
UserCreate
```

ni puede modificarse mediante:

```text
UserUpdate
```

Por lo tanto, un usuario no puede enviar:

```json
{
    "role": "ADMIN"
}
```

para convertirse en administrador.

El rol de administrador se asigna mediante un proceso controlado.

---

# Respuestas de la API

La aplicación utiliza una respuesta común:

```text
ApiResponse
```

Esto permite mantener una estructura consistente para las respuestas de los endpoints.

Por ejemplo:

```json
{
    "success": true,
    "message": "Inicio de sesión exitoso.",
    "data": {
        "access_token": "...",
        "token_type": "bearer"
    }
}
```

Los errores utilizan las excepciones personalizadas definidas en:

```text
app/core/exceptions.py
```

---

# Manejo de contraseñas

Las contraseñas nunca se almacenan en texto plano.

Durante el registro:

```text
password

   ↓
Argon2
   ↓
password_hash
   ↓
PostgreSQL
```

Durante el login:

```text
password ingresado
       ↓
verify_password()
       ↓
Argon2
       ↓
comparación con password_hash
```

La aplicación no devuelve el hash de contraseña mediante la API.

---

# Tests

Los tests de integración utilizan:

```text
pytest
```

y:

```text
FastAPI TestClient
```

La base de datos utilizada durante las pruebas es PostgreSQL independiente de la base de desarrollo.

---

# Ejecutar todos los tests

Desde:

```text
backend/
```

ejecutar:

```powershell
pytest -v
```

Resultado actual:

```text
103 passed
```

---

# Tests de autenticación

Archivo:

```text
tests/integration/routes/test_auth_routes.py
```

Actualmente cubre:

* Login exitoso.
* Password incorrecta.
* Usuario inexistente.
* Usuario inactivo.
* `sub` correcto.
* JWT utilizable en `/users/me`.
* No exposición de existencia de usuario ante credenciales inválidas.
* Usuario inactivo sin `access_token`.
* Claims obligatorios.
* Algoritmo configurado.
* Expiración configurada correctamente.

---

# Tests de usuarios y autorización

Archivo:

```text
tests/integration/routes/test_user_routes.py
```

Incluye pruebas para:

* `/users/me`.
* Autenticación requerida.
* USER.
* ADMIN.
* Acceso administrativo.
* Restricciones de rol.
* Activación.
* Desactivación lógica.
* Actualización.
* Tokens inválidos.
* Tokens expirados.
* Firma inválida.
* UUID inválido.
* `sub` ausente.
* Algoritmo incorrecto.
* Algoritmo `none`.
* Bearer inválido.
* Usuarios inexistentes/inactivos.

---

# Filosofía de testing

La estrategia actual es:

```text
Cambiar una funcionalidad
        ↓
Agregar pruebas
        ↓
Ejecutar pruebas específicas
        ↓
Corregir
        ↓
Ejecutar suite completa
        ↓
Continuar
```

Esto permite detectar rápidamente regresiones.

Los datos creados durante las pruebas utilizan identificadores únicos cuando es necesario para evitar colisiones entre tests.

---

# Decisiones de diseño actuales

## Registro público

El registro siempre crea:

```text
UserRole.USER
```

El cliente no controla el rol.

---

## Administración

Las operaciones administrativas están protegidas mediante:

```python
get_current_admin
```

---

## Eliminación

Los usuarios no se eliminan físicamente.

Se utiliza:

```text
is_active = False
```

---

## Autenticación

Se utiliza JWT stateless con expiración.

Actualmente no existe un sistema de refresh tokens ni blacklist.

---

## Contraseñas

Se utiliza Argon2 para almacenamiento seguro de contraseñas.

---

## Separación de responsabilidades

Las rutas no contienen la lógica de negocio principal.

La responsabilidad se divide entre:

```text
Routes
Controllers
Services
Repositories
Models
Schemas
Core
```

---

# Flujo completo de autenticación

## Registro

```text
POST /users
      │
      ▼
 UserController
      │
      ▼
 UserService
      │
      ▼
 hash_password()
      │
      ▼
 UserRepository
      │
      ▼
 PostgreSQL
```

---

## Login

```text
POST /auth/login
      │
      ▼
AuthController
      │
      ▼
AuthService
      │
      ├── UserRepository
      │
      ├── verify_password()
      │
      └── create_access_token()
                    │
                    ▼
                 JWT
```

---

## Endpoint protegido

```text
GET /users/me
      │
      ▼
 HTTPBearer
      │
      ▼
 get_current_user
      │
      ▼
 decode_access_token
      │
      ▼
 validar JWT
      │
      ▼
 UUID
      │
      ▼
 UserRepository
      │
      ▼
 usuario activo
      │
      ▼
 endpoint
```

---

## Endpoint administrativo

```text
GET /users
      │
      ▼
 get_current_admin
      │
      ▼
 get_current_user
      │
      ▼
 validar JWT
      │
      ▼
 buscar usuario
      │
      ▼
 verificar role
      │
      ├── ADMIN → continúa
      │
      └── USER  → 403
```

---

# Próximas etapas

La autenticación y autorización básica están actualmente consolidadas.

Los siguientes módulos pueden desarrollarse sobre esta base:

```text
┌─────────────────────────────┐
│ Autenticación               │
│ JWT + Roles + Users         │
│           ✓                 │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Próximo módulo SIHS         │
└──────────────┬──────────────┘
               │
               ▼
       nuevos módulos
       de negocio del SIHS
```

Antes de implementar nuevos módulos, se recomienda mantener el mismo patrón:

```text
Model
   ↓
Schema
   ↓
Repository
   ↓
Service
   ↓
Controller
   ↓
Route
   ↓
Tests
```

---

# Estado del proyecto

Actualmente el backend cuenta con una base funcional de:

```text
✓ FastAPI
✓ PostgreSQL
✓ SQLAlchemy
✓ Configuración mediante .env
✓ Arquitectura por capas
✓ Usuarios
✓ Roles
✓ Registro
✓ Login
✓ Argon2
✓ JWT
✓ Bearer Authentication
✓ Autorización ADMIN
✓ Usuarios activos/inactivos
✓ Desactivación lógica
✓ Manejo de excepciones
✓ Respuestas estandarizadas
✓ Tests de integración
✓ 103 tests pasando
```

La capa de **autenticación, JWT y autorización** se considera estable y lista para utilizarse como fundamento de los siguientes módulos funcionales del SIHS.
