# Prueba de Conexión al API

## Pasos para verificar la conexión

### 1. Verificar que el backend esté corriendo

Abre un navegador o usa curl/Postman:
```
http://localhost:8000/api/v1/
```

### 2. Cargar los datos (IMPORTANTE - hacer esto primero)

**Endpoint:**
```
POST http://localhost:8000/api/v1/load?min_similarity=0.3
```

**Con curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/load?min_similarity=0.3"
```

**Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Datos cargados y grafo construido",
  "statistics": {
    "total_songs": XXX,
    "total_connections": XXX,
    ...
  }
}
```

### 3. Probar el endpoint de canciones

```
GET http://localhost:8000/api/v1/songs?limit=50&offset=0&sort_by=popularity
```

**Con curl:**
```bash
curl "http://localhost:8000/api/v1/songs?limit=50&offset=0&sort_by=popularity"
```

## Si los endpoints no funcionan:

1. **Verifica el puerto del backend:**
   - ¿Está corriendo en el puerto 8000?
   - Si es 5000, cambia en `api_constants.dart`:
     ```dart
     static const String baseUrl = 'http://localhost:5000';
     static const String apiPrefix = '/api';
     ```

2. **Verifica el prefijo del API:**
   - Si tu backend usa `/api` (no `/api/v1`):
     ```dart
     static const String apiPrefix = '/api';
     ```

3. **Regenera el código:**
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```
