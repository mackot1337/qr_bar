import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [data, setData] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [error, setError] = useState('')
  const [inputType, setInputType] = useState('qr')
  const [barcodeType, setBarcodeType] = useState('code128')

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
        barcode_type: barcodeType
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
            /> Barcode
          </label>
        </div>

        {inputType === 'barcode' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label htmlFor="barcodeType">Barcode Format:</label>
            <select 
              id="barcodeType" 
              value={barcodeType} 
              onChange={(e) => setBarcodeType(e.target.value)}
              style={{ padding: '8px', fontSize: '16px' }}
            >
              <option value="code128">Code 128</option>
              <option value="code39">Code 39</option>
              <option value="ean13">EAN-13 (12 or 13 digits)</option>
              <option value="ean8">EAN-8 (7 or 8 digits)</option>
              <option value="isbn13">ISBN-13</option>
              <option value="upca">UPC-A (11 or 12 digits)</option>
            </select>
          </div>
        )}
        
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
