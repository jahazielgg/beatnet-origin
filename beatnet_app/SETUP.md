# BeatNet Flutter - Guía de Configuración

## Aplicación Flutter Profesional con Clean Architecture

Esta aplicación implementa un sistema de recomendación musical utilizando Clean Architecture, BLoC para gestión de estado, y se conecta al backend BeatNet.

---

## 🎯 Características Implementadas

### Arquitectura
- ✅ **Clean Architecture** (Presentation, Domain, Data)
- ✅ **BLoC Pattern** para gestión de estado
- ✅ **Dependency Injection** con GetIt
- ✅ **Repository Pattern**
- ✅ **Use Cases** para lógica de negocio

### Funcionalidades
- ✅ **Lista de canciones** con scroll infinito
- ✅ **Búsqueda** de canciones por título
- ✅ **Recomendaciones** basadas en similitud
- ✅ **Generación de playlists**:
  - Optimal (Backtracking)
  - Greedy (rápido)
  - Diverse (variado)
- ✅ **Visualización profesional** con Material 3

---

## 🚀 Pasos de Configuración

### 1. Ubicación del Proyecto

```
C:\Users\Jahaziel\Documents\2025-02\complejidad algoritmica\tf\beatnet\beatnet_app\
```

### 2. Verificar Backend

Asegúrate de que el backend esté corriendo:

```bash
cd ..\back\beatnet_backend
python main.py
```

El backend debe estar en: `http://localhost:5000`

### 3. Configurar URL del API

**Abre el archivo:**
```
lib/core/constants/api_constants.dart
```

**Modifica la línea 4:**

```dart
// Para emulador Android:
static const String baseUrl = 'http://10.0.2.2:5000';

// Para dispositivo físico (usa tu IP local):
static const String baseUrl = 'http://192.168.X.X:5000';

// Para iOS Simulator:
static const String baseUrl = 'http://localhost:5000';
```

**Encontrar tu IP:**
```bash
# Windows
ipconfig
# Buscar "IPv4 Address"

# Mac/Linux
ifconfig
# Buscar "inet"
```

### 4. Instalar Dependencias

```bash
flutter pub get
```

### 5. Ejecutar la App

```bash
flutter run
```

---

## 📱 Pantallas de la App

### Home Page
- Lista de canciones con scroll infinito
- Ordenamiento por: Popularidad, Título, Año
- Botón de búsqueda
- Navegación a detalles

### Song Details
- Cover de la canción ampliado
- Información: título, artista, géneros, duración, año, popularidad
- **3 botones de generación de playlists:**
  - 🌟 Óptima (Backtracking)
  - ⚡ Rápida (Greedy)
  - 🔀 Diversa (Mix variado)
- Lista de recomendaciones con porcentaje de similitud

### Search Page
- Campo de búsqueda
- Búsqueda fuzzy activada
- Resultado con navegación a detalles

### Playlist Page
- Carátula destacada
- Estadísticas: canciones, duración, similitud
- Indicador del algoritmo usado
- Lista completa de canciones con orden

---

## 🏗️ Estructura del Código

```
lib/
├── config/
│   └── theme/
│       └── app_theme.dart          # Tema Material 3
├── core/
│   ├── constants/
│   │   └── api_constants.dart      # URLs y constantes
│   ├── di/
│   │   └── injection_container.dart # Dependency injection
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   └── dio_client.dart         # Configuración de Dio
│   └── usecases/
│       └── usecase.dart            # Base para use cases
├── data/
│   ├── datasources/
│   │   └── beatnet_api_client.dart # Cliente Retrofit
│   ├── models/
│   │   └── *.dart                  # Modelos de datos
│   └── repositories/
│       └── song_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── *.dart                  # Entidades de dominio
│   ├── repositories/
│   │   └── song_repository.dart    # Interface del repositorio
│   └── usecases/
│       └── *.dart                  # Casos de uso
├── presentation/
│   ├── bloc/
│   │   ├── songs/                  # BLoC de canciones
│   │   ├── recommendations/        # BLoC de recomendaciones
│   │   ├── playlist/               # BLoC de playlists
│   │   └── search/                 # BLoC de búsqueda
│   ├── pages/
│   │   ├── home/                   # Pantalla principal
│   │   ├── song_details/           # Detalles de canción
│   │   ├── search/                 # Búsqueda
│   │   └── playlist/               # Playlist generada
│   └── widgets/
│       ├── song_card.dart          # Card de canción
│       └── loading_shimmer.dart    # Shimmer de carga
└── main.dart                       # Punto de entrada
```

---

## 🔧 Solución de Problemas

### Error de Conexión

```
DioException: Connection refused
```

**Solución:**
1. Verifica que el backend esté corriendo
2. Revisa la URL en `api_constants.dart`
3. Si usas emulador Android: usa `10.0.2.2`
4. Si usas dispositivo físico: verifica que estén en la misma red WiFi

### Carátulas no Cargan

Las URLs de las carátulas vienen del backend. Si no cargan:
- Verifica conexión a internet
- El backend debe tener URLs válidas en `songs.json`

### Backend no Carga Datos

Si ves error "No hay datos cargados":
1. Ejecuta el endpoint de carga:
```bash
POST http://localhost:5000/api/load?min_similarity=0.3
```
2. O usa Postman/Thunder Client para hacer la petición

---

## 📦 Dependencias Principales

```yaml
# Estado
flutter_bloc: ^8.1.6

# Networking
dio: ^5.7.0
retrofit: ^4.4.1

# DI
get_it: ^8.0.2

# UI
google_fonts: ^6.2.1
cached_network_image: ^3.4.1
shimmer: ^3.0.0

# Utils
dartz: ^0.10.1
equatable: ^2.0.5
```

---

## 🎨 Diseño

### Colores Principales
- **Primary**: Indigo (#6366F1)
- **Secondary**: Purple (#8B5CF6)
- **Accent**: Pink (#EC4899)
- **Background**: Dark Blue (#0F172A)

### Tipografías
- **Títulos**: Poppins
- **Cuerpo**: Inter

---

## 🚀 Próximos Pasos

1. **Ejecuta el backend** (debe estar en `localhost:5000`)
2. **Configura la URL** en `api_constants.dart`
3. **Ejecuta** `flutter run`
4. **Carga datos** mediante la app o Postman:
   - `POST /api/load?min_similarity=0.3`

---

## 👥 Equipo

- Julio Daniel Castro Alejos
- José Jahaziel Guerra Perez
- Gabriela Nicole Shapiama Rivera

**UPC** - Complejidad Algorítmica 2025-02

---

## 📝 Notas Importantes

- La app usa **Clean Architecture**, separa las capas correctamente
- Los **BLoCs** manejan todo el estado
- **Dependency Injection** hace el código testeable
- Usa **Repository Pattern** para abstraer la fuente de datos
- **Retrofit** genera el código del API client automáticamente

¡Disfruta de BeatNet! 🎵
