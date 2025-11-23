"""
Algoritmos de Ordenamiento
MergeSort, QuickSort, QuickSelect para ordenar canciones
"""
from typing import List, Callable
from models.song import Song

def merge_sort(songs: List[Song], key: Callable[[Song], any] = None, reverse: bool = False) -> List[Song]:
    """
    MERGE SORT O(n log n) - Divide y Conquista
    Ordena canciones de forma estable
    
    Args:
        songs: Lista de canciones a ordenar
        key: Función para extraer clave de comparación (ej: lambda s: s.popularity)
        reverse: Si True, ordena descendente
    
    Returns:
        Lista ordenada de canciones
    """
    if len(songs) <= 1:
        return songs.copy()
    
    # Función de comparación
    if key is None:
        key = lambda x: x.title
    
    def merge(left: List[Song], right: List[Song]) -> List[Song]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            left_val = key(left[i])
            right_val = key(right[j])
            
            if (left_val <= right_val) != reverse:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    # Dividir
    mid = len(songs) // 2
    left = merge_sort(songs[:mid], key, reverse)
    right = merge_sort(songs[mid:], key, reverse)
    
    # Conquistar (merge)
    return merge(left, right)


def quick_sort(songs: List[Song], key: Callable[[Song], any] = None, reverse: bool = False) -> List[Song]:
    """
    QUICK SORT O(n log n) promedio - Divide y Conquista
    Más rápido en práctica que MergeSort
    Usa particionamiento 3-way para manejar duplicados eficientemente

    Args:
        songs: Lista de canciones
        key: Función de comparación
        reverse: Orden descendente

    Returns:
        Lista ordenada
    """
    if len(songs) <= 1:
        return songs.copy()

    if key is None:
        key = lambda x: x.title

    songs_copy = songs.copy()

    def partition_3way(arr: List[Song], low: int, high: int) -> tuple:
        """
        3-way partitioning (Dutch National Flag)
        Retorna (lt, gt) donde:
        - arr[low..lt-1] < pivot
        - arr[lt..gt] == pivot
        - arr[gt+1..high] > pivot
        """
        if low >= high:
            return (low, high)

        # Pivot: elemento del medio para evitar peor caso con datos ordenados
        mid = low + (high - low) // 2
        arr[mid], arr[high] = arr[high], arr[mid]
        pivot = key(arr[high])

        lt = low  # Límite de elementos menores
        gt = high  # Límite de elementos mayores
        i = low

        while i <= gt:
            current_val = key(arr[i])

            if reverse:
                # Para orden descendente
                if current_val > pivot:
                    arr[lt], arr[i] = arr[i], arr[lt]
                    lt += 1
                    i += 1
                elif current_val < pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    gt -= 1
                else:
                    i += 1
            else:
                # Para orden ascendente
                if current_val < pivot:
                    arr[lt], arr[i] = arr[i], arr[lt]
                    lt += 1
                    i += 1
                elif current_val > pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    gt -= 1
                else:
                    i += 1

        return (lt, gt)

    def quick_sort_recursive(arr: List[Song], low: int, high: int):
        if low < high:
            lt, gt = partition_3way(arr, low, high)
            quick_sort_recursive(arr, low, lt - 1)
            quick_sort_recursive(arr, gt + 1, high)

    quick_sort_recursive(songs_copy, 0, len(songs_copy) - 1)
    return songs_copy


def quick_select(songs: List[Song], k: int, key: Callable[[Song], any] = None, reverse: bool = False) -> Song:
    """
    QUICK SELECT O(n) promedio - Encuentra el k-ésimo elemento
    Útil para encontrar "top K" sin ordenar toda la lista
    
    Args:
        songs: Lista de canciones
        k: Posición del elemento a encontrar (0-indexed)
        key: Función de comparación
        reverse: Si True, busca k-ésimo más grande
    
    Returns:
        La k-ésima canción según el criterio
    """
    if not songs or k < 0 or k >= len(songs):
        raise ValueError("Invalid k or empty list")
    
    if key is None:
        key = lambda x: x.popularity
    
    songs_copy = songs.copy()
    
    def partition(arr: List[Song], low: int, high: int) -> int:
        pivot = key(arr[high])
        i = low - 1
        
        for j in range(low, high):
            current_val = key(arr[j])
            
            if (current_val <= pivot) != reverse:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def select(arr: List[Song], low: int, high: int, k: int) -> Song:
        if low == high:
            return arr[low]
        
        pi = partition(arr, low, high)
        
        if k == pi:
            return arr[k]
        elif k < pi:
            return select(arr, low, pi - 1, k)
        else:
            return select(arr, pi + 1, high, k)
    
    return select(songs_copy, 0, len(songs_copy) - 1, k)


def get_top_k_songs(songs: List[Song], k: int, key: Callable[[Song], any] = None) -> List[Song]:
    """
    Obtiene las top K canciones usando QuickSelect (más eficiente que ordenar)
    Complejidad: O(n) promedio vs O(n log n) de ordenar
    
    Args:
        songs: Lista de canciones
        k: Número de canciones a retornar
        key: Criterio de ordenamiento (default: popularidad)
    
    Returns:
        Top K canciones ordenadas descendente
    """
    if not songs or k <= 0:
        return []
    
    if key is None:
        key = lambda x: x.popularity
    
    k = min(k, len(songs))
    
    # Encontrar el k-ésimo elemento más grande
    threshold_song = quick_select(songs, k - 1, key, reverse=True)
    threshold_value = key(threshold_song)
    
    # Filtrar canciones >= threshold
    top_songs = [s for s in songs if key(s) >= threshold_value]
    
    # Ordenar solo las top K
    return quick_sort(top_songs[:k], key, reverse=True)


def sort_by_multiple_criteria(songs: List[Song]) -> List[Song]:
    """
    Ordenamiento multi-criterio usando MergeSort estable
    Orden: 1) Popularidad DESC, 2) Año DESC, 3) Título ASC
    
    Returns:
        Lista ordenada
    """
    # Ordenar por título (último criterio)
    sorted_songs = merge_sort(songs, key=lambda s: s.title.lower(), reverse=False)
    
    # Ordenar por año (segundo criterio) - MergeSort es estable
    sorted_songs = merge_sort(sorted_songs, key=lambda s: s.year or 0, reverse=True)
    
    # Ordenar por popularidad (primer criterio)
    sorted_songs = merge_sort(sorted_songs, key=lambda s: s.popularity, reverse=True)
    
    return sorted_songs