import { Routes, Route, Navigate, useParams, Outlet } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import RoleProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
// import CandidateList from './pages/CandidateList'
// import CandidateDetail from './pages/CandidateDetail'
import './App.css'

function HomeRedirect() {
  const { user } = useAuth()

  if (!user) return <Navigate to="/login" replace />

  if (user.role === 'reviewer' || user.role === 'admin') {
    return <Navigate to="/candidates" replace />
  }

  return <Navigate to={`/candidates/${user.id}`} replace />
}

function CandidateList() {
    return (
        <div>
            <h2>Candidate List</h2>
            <p>This is the candidate list page.</p>
        </div>
    )
}

function CandidateDetail() {
    return (
        <div>
            <h2>Candidate Detail</h2>
            <p>This is the candidate detail page.</p>
        </div>
    )
}

function CandidateOwnerRoute() {
    let user = {id: 123}
    const id = useParams().id

    console.log(id, user.id)

    if (!user) {
        return <Navigate to="/login" replace />
    }

    if (user.id == id) {
        return <Outlet /> 
    }

    return <div>
        <h2>Access Denied</h2>
        <p>You are not the owner of this candidate profile.</p>
    </div>
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
</Route>
        <Route element={<CandidateOwnerRoute />}>
            <Route element={<Layout />}>
          <Route path="/candidates/:id" element={<CandidateDetail />} />
        </Route>
      </Route>

      <Route path="/" element={<HomeRedirect />} />
    </Routes>
  )
}

export default App
