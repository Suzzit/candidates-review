import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

function decodeToken(token) {
  try {
    const payload = token.split('.')[1]
    const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
    const data = JSON.parse(json)

    if (data.exp && data.exp * 1000 < Date.now()) {
      return null
    }

    return data
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('auth_token'))
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('auth_token')
    return stored ? decodeToken(stored) : null
  })

  const login = (newToken) => {
    const decoded = decodeToken(newToken)
    localStorage.setItem('auth_token', newToken)
    setToken(newToken)
    setUser(decoded)
    return decoded
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
