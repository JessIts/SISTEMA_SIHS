import { Outlet } from 'react-router-dom'
import './DashboardLayout.css'

function DashboardLayout() {
  return (
    <div className="dashboard-layout">

      <header className="dashboard-layout__header">
        Header
      </header>

      <div className="dashboard-layout__body">

        <aside className="dashboard-layout__sidebar">
          Sidebar
        </aside>

        <main className="dashboard-layout__content">
          <Outlet />
        </main>

      </div>

      <footer className="dashboard-layout__footer">
        Footer
      </footer>

    </div>
  )
}

export default DashboardLayout