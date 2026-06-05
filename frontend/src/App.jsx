import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [data, setData] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [error, setError] = useState('')
  const [inputType, setInputType] = useState('qr')

  const generateCode = async (e) => {
    e.preventDefault()
    if (!data) {
      setError('Please enter some text/data')
      return
    }
    try {
      setError('')
      setImageUrl('')
      
      const endpoint = inputType === 'qr' ? 'qr' : 'barcode'
      const payload = {
        data: data,
        fill_color: 'black',
        back_color: 'white',
        barcode_type: 'code128' // default used for barcode
      }
      
      const response = await axios.post(`http://localhost:8000/generate/${endpoint}`, payload)
      setImageUrl(response.data.image_url)
    } catch (err) {
      setError('Generation failed. Ensure the backend is running.')
      console.error(err)
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '400px', margin: '0 auto' }}>
      <h1>Code Generator</h1>
      
      <form onSubmit={generateCode} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input 
          type="text" 
          value={data} 
          onChange={(e) => setData(e.target.value)} 
          placeholder="Enter text or URL here" 
          style={{ padding: '10px', fontSize: '16px' }}
        />

        <div style={{ display: 'flex', gap: '10px' }}>
          <label>
            <input 
              type="radio" 
              value="qr" 
              checked={inputType === 'qr'} 
              onChange={(e) => setInputType(e.target.value)} 
            /> QR Code
          </label>
          <label>
            <input 
              type="radio" 
              value="barcode" 
              checked={inputType === 'barcode'} 
              onChange={(e) => setInputType(e.target.value)} 
            /> Barcode (Code128)
          </label>
        </div>
        
        <button type="submit" style={{ padding: '10px', fontSize: '16px', cursor: 'pointer' }}>
          Generate
        </button>
      </form>
      
      {error && <p style={{ color: 'red', marginTop: '15px' }}>{error}</p>}
      
      {imageUrl && (
        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <img 
            src={imageUrl} 
            alt="Generated Code" 
            style={{ maxWidth: '100%', border: '1px solid #ccc', padding: '10px', backgroundColor: 'white' }} 
          />
        </div>
      )}
    </div>
  )
}

export default App
