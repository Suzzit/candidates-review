import { Link, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Layout.css'

function Layout() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    return (
        <div className="app-shell">
            <header className="app-header">
                <h1>Candidate Review</h1>
                <nav className="app-nav">
                    <span className="app-user">
                        <strong>{user.name}</strong> ({user.role})
                    </span>
                    <button className="app-logout" onClick={handleLogout}>
                        Log out
                    </button>
                </nav>
            </header>
            <div className="app-content">
                <Outlet />
            </div>
        </div>
    )
}

export default Layout
