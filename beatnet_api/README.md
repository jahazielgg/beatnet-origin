# BeatNet API

Sistema de recomendación musical basado en algoritmos de grafos y técnicas de optimización.

**Proyecto académico** - Curso de Complejidad Algorítmica, Universidad Peruana de Ciencias Aplicadas (UPC)

**Equipo:** 

* Julio Daniel Castro Alejos
* José Jahaziel Guerra Perez
* Gabriela Nicole Shapiama Rivera

---

## Descripción

BeatNet es una API que implementa diversos algoritmos fundamentales de ciencias de la computación aplicados al dominio de recomendación musical. El sistema modela las canciones como un grafo ponderado donde los nodos representan canciones y las aristas representan similitud musical.

---

## Algoritmos Implementados

### 1. Construcción de Grafo (Fuerza Bruta)

* **Complejidad:** O(n²)
* Calcula similitud entre todas las parejas de canciones
* Construye grafo ponderado basado en similitud por género, popularidad y año

### 2. Algoritmos de Ordenamiento (Divide y Vencerás)

* **MergeSort:** O(n log n) - Ordenamiento estable
* **QuickSort:** O(n log n) promedio - Ordenamiento in-place
* **QuickSelect:** O(n) promedio - Encuentra k-ésimo elemento sin ordenar

### 3. Algoritmos de Búsqueda en Grafos

* **BFS (Breadth-First Search):** O(V + E) - Exploración por niveles
* **DFS (Depth-First Search):** O(V + E) - Exploración en profundidad
* **Dijkstra:** O((V + E) log V) - Camino de máxima similitud

### 4. Generación de Playlists

* **Backtracking con poda:** Playlists óptimas (máxima similitud acumulada)
* **Algoritmo Greedy:** Playlists rápidas (selección voraz)
* **Algoritmo Diverso:** Balance entre similitud y variedad de géneros

### 5. Visualización con Graphviz

* Grafo completo de conexiones
* Subgrafos centrados en canciones específicas
* Red de conexiones entre géneros musicales
* Visualización de playlists generadas

---

## Estructura del Proyecto

```
beatnet_backend/
├── data/
│   └── songs.json              # Dataset de canciones
│
├── models/
│   ├── song.py                 # Modelo Song con cálculo de similitud
│   └── graph.py                # Grafo y nodos
│
├── core/
│   ├── similarity.py           # Construcción de grafo, similitud
│   ├── search.py               # BFS, DFS, Dijkstra
│   ├── sorting.py              # MergeSort, QuickSort, QuickSelect
│   └── recommendations.py      # Backtracking, Greedy, Diverse
│
├── services/
│   ├── data_service.py         # Carga y gestión de datos
│   └── visualization_service.py # Generación de visualizaciones
│
├── api/
│   └── routes.py               # Endpoints REST
│
├── outputs/                    # Gráficos generados
│
├── main.py                     # Servidor Flask
├── test.py                     # Script de pruebas
├── requirements.txt
└── README.md
```

---

## Instalación

### 1. Clonar repositorio

bash

```bash
git clone <repositorio>
cd beatnet_backend
```

### 2. Crear entorno virtual

bash

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

bash

```bash
pip install -r requirements.txt
```

### 4. Instalar Graphviz (sistema)

**Windows:** Descargar de [https://graphviz.org/download/](https://graphviz.org/download/) y agregar a PATH

**Linux:** `sudo apt-get install graphviz`

**Mac:** `brew install graphviz`

### 5. Preparar datos

Colocar archivo `songs.json` en la carpeta `data/`

---

## Uso

### Iniciar servidor

bash

```bash
python main.py
```

El servidor estará disponible en: `http://localhost:5000`

### Ejecutar pruebas

bash

```bash
python test.py
```

Este script prueba todos los algoritmos implementados y genera visualizaciones en `outputs/`.

---

## Endpoints Principales

### Gestión de Datos

bash

```bash
POST /api/load?min_similarity=0.3
GET  /api/songs?limit=20&sort_by=popularity
GET  /api/songs/search?q=Girl
GET  /api/stats
```

### Recomendaciones

bash

```bash
GET  /api/recommendations/<song_id>?top_k=10
```

### Búsquedas en Grafo

bash

```bash
GET  /api/search/bfs/<song_id>?max_depth=3
GET  /api/search/dfs/<song_id>?max_depth=3
GET  /api/path/<start_id>/<end_id>
```

### Generación de Playlists

bash

```bash
POST /api/playlist/optimal?song_id=<id>&length=8&min_similarity=0.3
POST /api/playlist/greedy?song_id=<id>&length=8
POST /api/playlist/diverse?song_id=<id>&length=8&diversity=0.5
```

### Visualizaciones

bash

```bash
POST /api/visualize/subgraph/<song_id>?depth=2
POST /api/visualize/genres
```

### Ordenamiento

bash

```bash
GET  /api/top/popularity?k=10
```

---

## Formato del Dataset

json

```json
[
{
"id":"694427392",
"title":"The World",
"artist":"Babalos",
"album":"The World",
"genres":["Pop","Dance-Pop"],
"duration":298,
"year":2024,
"popularity":244546,
"deezer_id":694427392,
"deezer_link":"https://www.deezer.com/track/694427392",
"preview_url":"https://cdnt-preview.dzcdn.net/...",
"cover_small":"https://cdn-images.dzcdn.net/.../56x56.jpg",
"cover_medium":"https://cdn-images.dzcdn.net/.../250x250.jpg",
"cover_big":"https://cdn-images.dzcdn.net/.../500x500.jpg",
"cover_xl":"https://cdn-images.dzcdn.net/.../1000x1000.jpg"
}
]
```

## Troubleshooting

### Graphviz no funciona

bash

```bash
# Windows: Agregar a PATH
C:\Program Files\Graphviz\bin

# Verificar instalación
dot -V
```

### Error al cargar JSON

* Verificar que `data/songs.json` existe
* Validar formato JSON

### Backtracking muy lento

* Reducir `playlist_length` (probar con 4-5 canciones)
* Aumentar `min_similarity` (probar con 0.5)
* El timeout está configurado en 30 segundos con fallback automático a greedy

---

## Tecnologías

* **Python 3.8+**
* **Flask** - Framework web
* **Graphviz** - Visualización de grafos
* **NetworkX** - Análisis de grafos 
* **Matplotlib** - Gráficos estadísticos

---

## Equipo de Desarrollo

* Julio Daniel Castro Alejos
* José Jahaziel Guerra Perez

* Gabriela Nicole Shapiama Rivera
