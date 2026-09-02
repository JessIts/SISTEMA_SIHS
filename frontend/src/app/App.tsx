import './App.css'

import { AppRoutes } from './routes'
import { AuthProvider } from '../context/AuthContext'

function App() {
  return (
    <AuthProvider>
      <div className="app">
        <AppRoutes />
      </div>
    </AuthProvider>
  )
}

export default App