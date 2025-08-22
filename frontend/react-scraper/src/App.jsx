import { useState } from 'react'
import LoginButton from './components/LoginButton'
import ScraperDashboard from './components/ScraperDashboard'

export default function App() {
  const [user, setUser] = useState(null)

  const existingToken = localStorage.getItem('access')
  if (existingToken && !user) {
    setUser({ loggedIn: true })
  }

  return (
    <div className="app-root">
      <header className="header">
        <h1>React Scraper Assignment</h1>
        {!user && <LoginButton onLogin={setUser} />}
        {user && (
          <button onClick={() => { localStorage.removeItem('access'); setUser(null); }}>
            Logout
          </button>
        )}
      </header>

      <main>
        {user ? <ScraperDashboard /> : <div className="center">Please sign in with Google to continue.</div>}
      </main>
    </div>
  )
}
