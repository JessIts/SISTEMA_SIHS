import { Link } from 'react-router-dom'

import './StatCard.css'

interface StatCardProps {
  label: string
  value: number | string
  hint?: string
  to?: string
}

function StatCard({ label, value, hint, to }: StatCardProps) {
  const content = (
    <>
      <span className="stat-card__label">{label}</span>
      <strong className="stat-card__value">{value}</strong>
      {hint && <span className="stat-card__hint">{hint}</span>}
    </>
  )

  if (to) {
    return (
      <Link to={to} className="stat-card stat-card--link">
        {content}
      </Link>
    )
  }

  return <div className="stat-card">{content}</div>
}

export default StatCard
