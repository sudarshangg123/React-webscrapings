import axios from 'axios'

export function apiInstance() {
  const token = localStorage.getItem('access')
  return axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
}
