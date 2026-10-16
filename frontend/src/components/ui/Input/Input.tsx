import type { InputHTMLAttributes } from 'react'

import './Input.css'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
}

function Input({
  label,
  error,
  id,
  ...props
}: InputProps) {
  return (
    <div className="input-field">
      <label
        htmlFor={id}
        className="input-field__label"
      >
        {label}
      </label>

      <input
        id={id}
        className={`input-field__input ${
          error ? 'input-field__input--error' : ''
        }`}
        {...props}
      />

      {error && (
        <span className="input-field__error">
          {error}
        </span>
      )}
    </div>
  )
}

export default Input