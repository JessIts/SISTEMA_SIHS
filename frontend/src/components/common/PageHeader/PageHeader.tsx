import type { ReactNode } from 'react'

import './PageHeader.css'

interface PageHeaderProps {
  title: string
  description?: ReactNode
  actions?: ReactNode
}

function PageHeader({
  title,
  description,
  actions,
}: PageHeaderProps) {
  return (
    <div className="page-header">
      <div className="page-header__text">
        <h1>{title}</h1>

        {description && <p>{description}</p>}
      </div>

      {actions && (
        <div className="page-header__actions">
          {actions}
        </div>
      )}
    </div>
  )
}

export default PageHeader
