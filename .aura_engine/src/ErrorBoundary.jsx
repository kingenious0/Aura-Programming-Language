import React from 'react';
class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { hasError: false, error: null }; }
  static getDerivedStateFromError(error) { return { hasError: true, error }; }
  render() { if (this.state.hasError) return <div className='p-10 text-red-500'>Aura Error: {this.state.error.toString()}</div>; return this.props.children; }
}
export default ErrorBoundary;