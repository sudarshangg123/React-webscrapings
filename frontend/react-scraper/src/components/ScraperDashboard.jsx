import { useEffect, useState } from 'react'
import { apiInstance } from '../api'

export default function ScraperDashboard() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [url, setUrl] = useState('https://example.com')

  const api = apiInstance()

  useEffect(() => { fetchItems() }, [])

  async function fetchItems() {
    try {
      const res = await api.get('/api/items/')
      setItems(res.data)
    } catch (e) {
      console.error(e)
    }
  }

  async function handleScrape() {
    setLoading(true)
    try {
      const res = await api.post('/api/scrape/', { url })
      setItems(prev => [...res.data, ...prev])
    } catch (e) {
      console.error(e)
      alert('Scrape failed — check console')
    }
    setLoading(false)
  }

  return (
    <div className="dashboard">
      <div className="controls">
        <input value={url} onChange={e => setUrl(e.target.value)} placeholder="Enter site URL to scrape" />
        <button onClick={handleScrape} disabled={loading}>{loading ? 'Fetching...' : 'Fetch Latest'}</button>
      </div>

      <div className="grid">
        {items.map(it => (
          <div key={it.id} className="card">
            <h3>{it.title}</h3>
            {it.url && <a href={it.url} target="_blank" rel="noreferrer">Open source</a>}
            <p className="meta">{it.source} • {new Date(it.scraped_at).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
