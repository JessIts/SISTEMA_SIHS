import { NavLink } from 'react-router-dom'

import { useAuth } from '../../../hooks/useAuth'
import { NAVIGATION } from '../../../utils/navigation'

import './Sidebar.css'

function Sidebar() {
  const { user } = useAuth()

  const sections = user ? NAVIGATION[user.role] ?? [] : []

  return (
    <aside className="sidebar">
      <nav className="sidebar__navigation">
        {sections.map((section, index) => (
          <div
            key={section.title ?? `section-${index}`}
            className="sidebar__section"
          >
            {section.title && (
              <span className="sidebar__section-title">
                {section.title}
              </span>
            )}

            {section.links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                title={link.label}
                className={({ isActive }) =>
                  `sidebar__link ${
                    isActive
                      ? 'sidebar__link--active'
                      : ''
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </div>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
