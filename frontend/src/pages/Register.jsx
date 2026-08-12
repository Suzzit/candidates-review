import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'
import { registerCandidate } from '../api/auth.js'
import './Auth.css'

function Register() {
    const { user } = useAuth()
    const navigate = useNavigate()
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [roleApplied, setRoleApplied] = useState('reviewer')
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)
    const [loading, setLoading] = useState(false)

    if (user) {
        return <Navigate to="/" replace />
    }

    async function handleSubmit(event) {
        event.preventDefault()
        setError(null)
        setSuccess(null)
        setLoading(true)

        try {
            const data = await registerCandidate({ name, email, password, roleApplied })
            setSuccess(data.message || 'Registration successful. You can now log in.')
            setName('')
            setEmail('')
            setPassword('')
            setRoleApplied('reviewer')
            setTimeout(() => navigate('/login'), 1200)
        } catch (err) {
            setError(err.message || 'Registration failed. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1>Register</h1>
                <p className="auth-subtitle">Create a new account to access the candidate review system.</p>

                {error && <div className="auth-error">{error}</div>}
                {success && <div className="auth-success">{success}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="auth-field">
                        <label htmlFor="name">Full Name</label>
                        <input
                            id="name"
                            type="text"
                            value={name}
                            onChange={(event) => setName(event.target.value)}
                            required
                        />
                    </div>

                    <div className="auth-field">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                            autoComplete="email"
                        />
                    </div>

                    <div className="auth-field">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            required
                            autoComplete="new-password"
                        />
                    </div>

                    <div className="auth-field">
                        <label htmlFor="roleApplied">Role Applied</label>
                        <select
                            id="roleApplied"
                            value={roleApplied}
                            onChange={(event) => setRoleApplied(event.target.value)}
                            required
                        >
                            <option value="reviewer">Reviewer</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>

                    <button className="auth-submit" type="submit" disabled={loading}>
                        {loading ? 'Registering…' : 'Register'}
                    </button>
                </form>

                <p className="auth-switch">
                    Already have an account? <Link to="/login">Login here</Link>.
                </p>
            </div>
        </div>
    )
}

export default Register
