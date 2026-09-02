import './Sidebar.css'

function Sidebar() {
  return (
    <aside className="sidebar">
      <nav className="sidebar__navigation">
        <a href="/" className="sidebar__link">
          Dashboard
        </a>

        <a href="/users" className="sidebar__link">
          Usuarios
        </a>
      </nav>
    </aside>
  )
}

export default Sidebar