import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function RoleProtectedRoute({ roles }) {
    let { user } = useAuth()

    if (!user) {
        return <Navigate to="/login" replace />
    }

    if (roles && roles.includes(user.role)) {
        return <Outlet />
    }

    return <div style={{ padding: '1rem' }}>
        <h2>Access Denied</h2>
        <p>You do not have permission to view this page.</p>
    </div>
}

export default RoleProtectedRoute
