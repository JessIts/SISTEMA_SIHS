const API_BASE_URL = 'http://localhost:8000/api/v1'

interface ApiError {
  message: string
}

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const headers = new Headers(options?.headers)

  headers.set('Content-Type', 'application/json')

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers,
      credentials: 'include',
    },
  )

  if (!response.ok) {
    let errorMessage = 'Ocurrió un error en la solicitud.'

    try {
      const error: ApiError = await response.json()

      if (error.message) {
        errorMessage = error.message
      }
    } catch {
      // El backend no devolvió un error JSON válido.
    }

    throw new Error(errorMessage)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}