# SISTEMA SIHS — Frontend

Frontend del **Sistema SIHS**, desarrollado con **React, TypeScript y Vite**.

Actualmente el frontend se encuentra en la etapa inicial de implementación y ya cuenta con la estructura y funcionalidad correspondiente al **inicio de sesión (Login)**.

---

## 🚀 Tecnologías utilizadas

* **React**
* **TypeScript**
* **Vite**
* **CSS**
* **Fetch API** para comunicación con el backend
* **ESLint** para validación del código

---

## 📁 Estructura actual

La estructura principal del frontend se organiza de la siguiente manera:

```text
frontend/
├── public/
├── src/
│   ├── assets/
│   │   ├── hero.png
│   │   ├── react.svg
│   │   └── vite.svg
│   │
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── ...
│
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── README.md
```

La estructura podrá evolucionar a medida que se incorporen nuevos módulos y componentes al sistema.

---

# 🔐 Login

La primera funcionalidad desarrollada del frontend es el **inicio de sesión**.

El objetivo del login es permitir que un usuario registrado en el backend pueda autenticarse desde la interfaz web.

El flujo general es:

```text
Usuario
   │
   ▼
Formulario de Login
   │
   ▼
Frontend React
   │
   ▼
API FastAPI
   │
   ▼
Autenticación
   │
   ▼
Respuesta del Backend
   │
   ▼
Frontend
```

---

## 🧩 Funcionalidades implementadas

Actualmente el frontend cuenta con:

* Interfaz de inicio de sesión.
* Campos para las credenciales del usuario.
* Manejo del estado del formulario.
* Comunicación con el backend.
* Procesamiento de la respuesta del backend.
* Manejo de autenticación exitosa.
* Manejo de errores de autenticación.
* Integración inicial entre frontend y backend.
* Validación de funcionamiento mediante pruebas.

---

# 🔗 Integración con el Backend

El frontend está diseñado para comunicarse con el backend desarrollado en **FastAPI**.

La arquitectura actual es:

```text
┌──────────────────────┐
│      React/Vite      │
│      Frontend        │
└──────────┬───────────┘
           │
           │ HTTP
           ▼
┌──────────────────────┐
│       FastAPI        │
│       Backend        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      PostgreSQL      │
│       Database       │
└──────────────────────┘
```

El frontend no maneja directamente la base de datos. Todas las operaciones relacionadas con usuarios, autenticación, roles y demás información del sistema se realizan a través de la API.

---

# 👤 Usuarios y roles

El sistema contempla usuarios con diferentes **roles**.

Los roles pertenecen al modelo de usuarios del backend y son almacenados en la base de datos.

Por lo tanto:

```text
PostgreSQL
    │
    ▼
Usuario
    │
    ├── Información personal
    ├── Credenciales
    └── Rol
          │
          ▼
      Autorización
```

El frontend utilizará posteriormente la información de autenticación y autorización proporcionada por el backend para controlar el acceso a las diferentes partes del sistema.

> La implementación completa de las interfaces y restricciones visuales según el rol todavía está pendiente.

---

# 🧪 Pruebas

Durante el desarrollo se realizaron pruebas sobre la funcionalidad implementada.

Actualmente:

* Las pruebas relacionadas con el login/autenticación implementadas hasta este punto funcionan correctamente.
* Las **3 pruebas ejecutadas durante esta etapa pasaron satisfactoriamente**.
* Vite compila correctamente el proyecto.

Esto confirma que la implementación actual del frontend se encuentra funcionando correctamente antes de continuar con los siguientes módulos.

---

# ⚙️ Instalación

## 1. Instalar dependencias

Desde la carpeta del frontend:

```bash
npm install
```

---

## 2. Ejecutar en modo desarrollo

```bash
npm run dev
```

Vite iniciará el servidor de desarrollo y mostrará la dirección local correspondiente.

Normalmente:

```text
http://localhost:5173
```

---

## 3. Compilar para producción

```bash
npm run build
```

---

## 4. Verificar el código

```bash
npm run lint
```

---

# 🔄 Estado actual del proyecto

### Frontend

| Funcionalidad              | Estado                              |
| -------------------------- | ----------------------------------- |
| Configuración React + Vite | ✅ Completado                        |
| TypeScript                 | ✅ Completado                        |
| Estructura inicial         | ✅ Completado                        |
| Interfaz Login             | ✅ Completado                        |
| Comunicación con Backend   | ✅ Implementada                      |
| Autenticación              | ✅ Implementación inicial completada |
| Pruebas del Login          | ✅ Completadas                       |
| Compilación Vite           | ✅ Correcta                          |
| Manejo de roles en UI      | ⏳ Pendiente                         |
| Protección de rutas        | ⏳ Pendiente                         |
| Dashboard                  | ⏳ Pendiente                         |
| Módulos del sistema        | ⏳ Pendiente                         |

---

# 🛠️ Próximos pasos

Una vez terminado el Login, el desarrollo del frontend continuará con la construcción progresiva del sistema.

Entre los siguientes pasos se encuentran:

1. Consolidar el manejo de autenticación.
2. Implementar la protección de rutas.
3. Manejar correctamente la sesión del usuario.
4. Integrar la información del usuario autenticado.
5. Implementar autorización basada en roles.
6. Crear el layout principal de la aplicación.
7. Crear el dashboard.
8. Implementar los diferentes módulos del Sistema SIHS.
9. Conectar cada módulo con los endpoints correspondientes del backend.
10. Agregar pruebas para las nuevas funcionalidades.

---

# 📌 Estado del desarrollo

**Estado actual:**

```text
Backend
████████░░ En desarrollo

Frontend
███░░░░░░░ Login completado
```

El **Login del frontend está terminado y funcionando**, por lo que el proyecto está listo para continuar con la siguiente etapa de desarrollo de la aplicación.

---

## 👨‍💻 Desarrollo

**Proyecto:** SISTEMA SIHS
**Frontend:** React + TypeScript + Vite
**Backend:** FastAPI
**Base de datos:** PostgreSQL
