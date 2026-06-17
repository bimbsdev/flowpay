import React, { ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
    // You can log to error reporting service here
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen bg-red-50">
          <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex-shrink-0">
                <svg
                  className="h-8 w-8 text-red-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4v2m0 4v2M9 3h6v0M9 3H6a3 3 0 00-3 3v12a3 3 0 003 3h12a3 3 0 003-3V6a3 3 0 00-3-3h-3"
                  />
                </svg>
              </div>
              <h1 className="text-lg font-semibold text-gray-900">Oops! Something went wrong</h1>
            </div>
            <p className="text-sm text-gray-600 mb-4">
              We're sorry for the inconvenience. An unexpected error has occurred.
            </p>
            {this.state.error && (
              <div className="bg-gray-100 p-3 rounded mb-4 max-h-32 overflow-auto">
                <p className="text-xs font-mono text-gray-700 whitespace-pre-wrap">
                  {this.state.error.message}
                </p>
              </div>
            )}
            <div className="flex gap-3">
              <button
                onClick={() => window.location.reload()}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                Reload Page
              </button>
              <button
                onClick={() => window.history.back()}
                className="flex-1 bg-gray-200 text-gray-900 py-2 px-4 rounded hover:bg-gray-300 transition-colors text-sm font-medium"
              >
                Go Back
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
