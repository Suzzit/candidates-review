import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import RoleProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import CandidateList from './pages/CandidateList'
import CandidateDetail from './pages/CandidateDetail'
import './App.css'

function HomeRedirect() {
  const { user } = useAuth()

  if (!user) return <Navigate to="/login" replace />

  if (user.role === 'reviewer' || user.role === 'admin') {
    return <Navigate to="/candidates" replace />
  }

  return <Navigate to={`/candidates/${user.id}`} replace />
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

        <Route element={<RoleProtectedRoute  roles={['reviewer', 'admin']} />}>
        <Route element={<Layout />}>
            <Route path="/candidates" element={<CandidateList />} />
          </Route>
          <Route path="/candidates/:id" element={<CandidateDetail />} />
        </Route>
      </Route>

      <Route path="/" element={<HomeRedirect />} />
    </Routes>
  )
}

export default App
