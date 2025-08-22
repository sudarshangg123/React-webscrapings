import { GoogleLogin } from '@react-oauth/google'
import axios from 'axios'

export default function LoginButton({ onLogin }) {
  const handleSuccess = async (credentialResponse) => {
    try {
      const id_token = credentialResponse.credential
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/auth/google/`, { id_token })
      const access = res.data.access
      localStorage.setItem('access', access)
      onLogin(res.data.user || { email: res.data.user?.email })
    } catch (err) {
      console.error('Login error', err)
      alert('Login failed')
    }
  }

  return (
    <div>
      <GoogleLogin onSuccess={handleSuccess} onError={() => console.log('Login Failed')} />
    </div>
  )
}
