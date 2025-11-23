# BeatNet - Sistema de Recomendación Musical Inteligente

Sistema completo de recomendación musical basado en algoritmos de grafos y técnicas de optimización, con backend API REST y aplicación móvil Flutter.

**Proyecto académico** - Curso de Complejidad Algorítmica, Universidad Peruana de Ciencias Aplicadas (UPC)

## Equipo

* Julio Daniel Castro Alejos
* José Jahaziel Guerra Perez
* Gabriela Nicole Shapiama Rivera

---

## Descripción General

BeatNet es un sistema completo que combina:

- **Backend API** (`beatnet_api`): Servidor Flask que implementa algoritmos fundamentales de ciencias de la computación aplicados a recomendación musical
- **Aplicación Móvil** (`beatnet_app`): Cliente Flutter multiplataforma con interfaz moderna y fluida

El sistema modela las canciones como un grafo ponderado donde los nodos representan canciones y las aristas representan similitud musical basada en género, popularidad y año.

---

## Estructura del Proyecto

```
beatnet/
├── beatnet_api/          # Backend API REST (Python/Flask)
│   ├── data/            # Dataset de canciones
│   ├── models/          # Modelos de datos
│   ├── core/            # Algoritmos implementados
│   ├── services/        # Servicios de datos y visualización
│   ├── api/             # Endpoints REST
│   └── outputs/         # Visualizaciones generadas
│
├── beatnet_app/         # Aplicación móvil (Flutter)
│   ├── lib/
│   │   ├── core/       # Configuración e inyección de dependencias
│   │   ├── data/       # Modelos y datasources
│   │   ├── domain/     # Entidades y casos de uso
│   │   ├── presentation/ # UI con BLoC
│   │   └── config/     # Temas y configuración
│   └── ...
│
├── .gitignore
└── README.md
```

---

## Características Principales

### Backend (beatnet_api)

#### Algoritmos Implementados

1. **Construcción de Grafo** - O(n²) - Fuerza bruta
2. **Ordenamiento**:
   - MergeSort - O(n log n)
   - QuickSort - O(n log n)
   - QuickSelect - O(n)
3. **Búsqueda en Grafos**:
   - BFS - O(V + E)
   - DFS - O(V + E)
   - Dijkstra - O((V + E) log V)
4. **Generación de Playlists**:
   - Backtracking con poda
   - Algoritmo Greedy
   - Algoritmo Diverso
5. **Visualización con Graphviz**

### Aplicación Móvil (beatnet_app)

- Arquitectura Clean Architecture con BLoC
- Navegación fluida entre canciones
- Búsqueda en tiempo real
- Visualización de recomendaciones
- Detalles de canciones con información completa
- Diseño responsivo y adaptado para móviles
- Tema oscuro con gradientes personalizados

---

## Instalación

### Requisitos Previos

- **Backend**: Python 3.8+, Graphviz
- **App**: Flutter 3.0+, Dart 2.17+

### Backend API

```bash
cd beatnet_api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar Graphviz (sistema)
# Windows: Descargar de https://graphviz.org/download/
# Linux: sudo apt-get install graphviz
# Mac: brew install graphviz

# Iniciar servidor
python main.py
```

El servidor estará en `http://localhost:5000`

### Aplicación Móvil

```bash
cd beatnet_app

# Instalar dependencias
flutter pub get

# Ejecutar en dispositivo/emulador
flutter run

# Build para producción
flutter build apk  # Android
flutter build ios  # iOS
```

---

## Configuración

### Backend

Asegúrate de tener el archivo `data/songs.json` con el dataset de canciones.

### App

Configurar la URL del backend en `lib/core/constants/api_constants.dart`:

```dart
class ApiConstants {
  static const String baseUrl = 'http://localhost:5000/api';
  // Para dispositivos físicos, usar IP local: 'http://192.168.x.x:5000/api'
}
```

---

## Uso

### API Endpoints Principales

```bash
# Cargar datos
POST /api/load?min_similarity=0.3

# Obtener canciones
GET /api/songs?limit=20&sort_by=popularity

# Buscar canciones
GET /api/songs/search?q=Girl

# Recomendaciones
GET /api/recommendations/<song_id>?top_k=10

# Búsqueda en grafo
GET /api/search/bfs/<song_id>?max_depth=3

# Generar playlist
POST /api/playlist/optimal?song_id=<id>&length=8
POST /api/playlist/greedy?song_id=<id>&length=8
POST /api/playlist/diverse?song_id=<id>&length=8

# Visualizaciones
POST /api/visualize/subgraph/<song_id>?depth=2
```

### Aplicación Móvil

1. **Pantalla Principal**: Explora el catálogo de canciones con opciones de ordenamiento
2. **Búsqueda**: Encuentra canciones por título, artista o álbum
3. **Detalles**: Ve información completa y recomendaciones similares
4. **Playlists**: Genera playlists inteligentes basadas en tus preferencias

---

## Tecnologías

### Backend
- Python 3.8+
- Flask - Framework web
- Graphviz - Visualización de grafos
- NetworkX - Análisis de grafos
- Matplotlib - Gráficos estadísticos

### Frontend
- Flutter 3.0+
- Dart 2.17+
- BLoC - Gestión de estado
- Dio - Cliente HTTP
- Get It - Inyección de dependencias
- Freezed - Modelos inmutables

---

## Documentación Adicional

- [Backend API - README completo](beatnet_api/README.md)
- Documentación de arquitectura Flutter en el código fuente

---

## Troubleshooting

### Backend

**Graphviz no funciona**
```bash
# Agregar a PATH en Windows
C:\Program Files\Graphviz\bin

# Verificar instalación
dot -V
```

**Backtracking muy lento**
- Reducir `playlist_length` (4-5 canciones)
- Aumentar `min_similarity` (0.5)

### App

**Error de conexión**
- Verificar que el backend está ejecutándose
- Usar IP local en lugar de localhost para dispositivos físicos
- Verificar firewall/permisos de red

**Error en build**
```bash
flutter clean
flutter pub get
flutter run
```

---

## Licencia

Proyecto académico - UPC 2025

---

## Contacto

Para preguntas o contribuciones, contactar al equipo de desarrollo.
