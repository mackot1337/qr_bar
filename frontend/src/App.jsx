import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [data, setData] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [error, setError] = useState('')
  const [inputType, setInputType] = useState('qr')
  const [barcodeType, setBarcodeType] = useState('code128')
  const [fillColor, setFillColor] = useState('#000000')
  const [backColor, setBackColor] = useState('#ffffff')
  const [logoBase64, setLogoBase64] = useState('')
  const [logoName, setLogoName] = useState('')
  const [logoPreview, setLogoPreview] = useState('')
  
  const [history, setHistory] = useState([])
  const [totalHistory, setTotalHistory] = useState(0)
  
  const [skip, setSkip] = useState(0)
  const limit = 5 

  const fetchHistory = async (currentSkip = skip) => {
    try {
      const response = await axios.get(`http://localhost:8000/history?limit=${limit}&skip=${currentSkip}`)
      setHistory(response.data.items || [])
      setTotalHistory(response.data.total || 0)
    } catch (err) {
      console.error('Nie udało się pobrać historii:', err)
    }
  }

  useEffect(() => {
    fetchHistory(skip)
  }, [skip])

  const handleLogoUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setLogoName(file.name)
      const reader = new FileReader()
      reader.onloadend = () => {
        setLogoPreview(reader.result)
        const base64String = reader.result.split(',')[1]
        setLogoBase64(base64String)
      }
      reader.readAsDataURL(file)
    } else {
      setLogoName('')
      setLogoBase64('')
      setLogoPreview('')
    }
  }

  const generateCode = async (e) => {
    e.preventDefault()
    
    if (!data) {
      setError('Proszę wprowadzić tekst lub adres URL')
      return
    }

    if (inputType === 'barcode') {
      const isNumeric = /^\d+$/.test(data);
      if (barcodeType === 'ean13' && (!isNumeric || (data.length !== 12 && data.length !== 13))) {
        setError('Błąd: EAN-13 wymaga dokładnie 12 lub 13 cyfr.');
        return;
      }
      if (barcodeType === 'ean8' && (!isNumeric || (data.length !== 7 && data.length !== 8))) {
        setError('Błąd: EAN-8 wymaga dokładnie 7 lub 8 cyfr.');
        return;
      }
      if (barcodeType === 'upca' && (!isNumeric || (data.length !== 11 && data.length !== 12))) {
        setError('Błąd: UPC-A wymaga dokładnie 11 lub 12 cyfr.');
        return;
      }
      if (barcodeType === 'isbn13' && (!isNumeric || data.length !== 13)) {
        setError('Błąd: ISBN-13 wymaga dokładnie 13 cyfr.');
        return;
      }
    }

    try {
      setError('')
      setImageUrl('')
      
      const endpoint = inputType === 'qr' ? 'qr' : 'barcode'
      const payload = {
        data: data,
        fill_color: fillColor,
        back_color: backColor,
        barcode_type: barcodeType,
        ...(inputType === 'qr' && logoBase64 ? { 
          logo_base64: logoBase64,
          logo_name: logoName
        } : {})
      }
      
      const response = await axios.post(`http://localhost:8000/generate/${endpoint}`, payload)
      setImageUrl(response.data.image_url)
      
      if (skip !== 0) {
        setSkip(0)
      } else {
        fetchHistory(0)
      }
      
    } catch (err) {
      console.error(err)

      if (err.response && err.response.status === 422) {
        const detail = err.response.data.detail;
        
        if (Array.isArray(detail)) {
          setError(`Błąd formatu: ${detail[0].msg}`);
        } 
        else if (typeof detail === 'string') {
          setError(`Uwaga: ${detail}`);
        } 
        else {
          setError('Nieprawidłowe dane. Sprawdź formularz.');
        }
      } else {
        setError('Wystąpił błąd serwera lub brak połączenia z API.');
      }
    }
  }

  const restoreAndPreviewFromHistory = (item) => {
    setError('');
    
    setData(item.data);
    const codeTypeLower = item.code_type.toLowerCase();
    setInputType(codeTypeLower);
    setFillColor(item.fill_color);
    setBackColor(item.back_color);
    if (item.barcode_type) setBarcodeType(item.barcode_type);

    if (codeTypeLower === 'qr') {
      if (item.logo_base64) {
        setLogoBase64(item.logo_base64);
        setLogoPreview(`data:image/png;base64,${item.logo_base64}`);
        setLogoName(item.logo_name || 'logo_z_historii.png');
      } else {
        setLogoName('');
        setLogoBase64('');
        setLogoPreview('');
      }
    }

    if (item.image_base64) {
      setImageUrl(`data:image/png;base64,${item.image_base64}`);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Code Generator</h1>
        <p className="subtitle">Zaawansowany kreator spersonalizowanych kodów QR i kreskowych</p>
      </header>
      
      <div className="dashboard-grid">
        <div className="card main-card">
          <h2 className="card-title">Konfiguracja kodu</h2>
          <form onSubmit={generateCode} className="modern-form">
            <div className="form-group">
              <label>Tekst lub adres URL:</label>
              <input 
                type="text" 
                value={data} 
                onChange={(e) => setData(e.target.value)} 
                placeholder="np. https://mojastrona.pl" 
                className="modern-input"
              />
            </div>

            <div className="form-group">
              <label>Typ kodu:</label>
              <div className="radio-tile-group">
                <label className={`radio-tile ${inputType === 'qr' ? 'active' : ''}`}>
                  <input 
                    type="radio" 
                    value="qr" 
                    checked={inputType === 'qr'} 
                    onChange={(e) => setInputType(e.target.value)} 
                    className="hidden-radio"
                  />
                  <span>Kod QR</span>
                </label>
                <label className={`radio-tile ${inputType === 'barcode' ? 'active' : ''}`}>
                  <input 
                    type="radio" 
                    value="barcode" 
                    checked={inputType === 'barcode'} 
                    onChange={(e) => setInputType(e.target.value)} 
                    className="hidden-radio"
                  />
                  <span>Kod Kreskowy</span>
                </label>
              </div>
            </div>

            <div className="color-pickers-row">
              <div className="form-group flex-1">
                <label>Kolor wypełnienia:</label>
                <div className="color-picker-wrapper">
                  <input type="color" value={fillColor} onChange={(e) => setFillColor(e.target.value)} className="modern-color-input" />
                  <input type="text" value={fillColor} onChange={(e) => setFillColor(e.target.value)} className="color-text-input" />
                </div>
              </div>
              <div className="form-group flex-1">
                <label>Kolor tła:</label>
                <div className="color-picker-wrapper">
                  <input type="color" value={backColor} onChange={(e) => setBackColor(e.target.value)} className="modern-color-input" />
                  <input type="text" value={backColor} onChange={(e) => setBackColor(e.target.value)} className="color-text-input" />
                </div>
              </div>
            </div>

            {inputType === 'barcode' && (
              <div className="form-group animate-fade">
                <label htmlFor="barcodeType">Format kodu kreskowego:</label>
                <select id="barcodeType" value={barcodeType} onChange={(e) => setBarcodeType(e.target.value)} className="modern-select">
                  <option value="code128">Code 128 (Uniwersalny)</option>
                  <option value="code39">Code 39</option>
                  <option value="ean13">EAN-13 (12 lub 13 cyfr)</option>
                  <option value="ean8">EAN-8 (7 lub 8 cyfr)</option>
                  <option value="isbn13">ISBN-13 (Książki)</option>
                  <option value="upca">UPC-A</option>
                </select>
              </div>
            )}

            {inputType === 'qr' && (
              <div className="form-group logo-upload-box animate-fade">
                <label className="logo-box-title">Osadź Logo (Opcjonalnie)</label>
                <div className="file-input-wrapper">
                  <button type="button" className="btn-secondary">Wybierz plik logo</button>
                  <input type="file" accept="image/*" onChange={handleLogoUpload} className="hidden-file-input" />
                </div>
                {logoName && (
                  <div className="logo-details">
                    {logoPreview && <img src={logoPreview} alt="Podgląd Logo" className="logo-micro-preview" />}
                    <span className="logo-name" title={logoName}>📄 {logoName}</span>
                  </div>
                )}
              </div>
            )}
            
            <button type="submit" className="btn-primary">Generuj Kod</button>
          </form>
          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="right-column">
          <div className="card preview-card">
            <h2 className="card-title">Podgląd wyniku</h2>
            {imageUrl ? (
              <div className="image-output-container animate-scale">
                <img src={imageUrl} alt="Wygenerowany Kod" className="generated-image" />
                <a href={imageUrl} download={`kod-${inputType}.png`} className="btn-download">💾 Pobierz plik obrazu</a>
              </div>
            ) : (
              <div className="preview-placeholder">
                <div className="placeholder-icon">📷</div>
                <p>Skonfiguruj parametry po lewej stronie i kliknij przycisk, aby wygenerować podgląd.</p>
              </div>
            )}
          </div>

          <div className="card history-card">
            <div className="history-card-header">
              <h2 className="card-title">Historia kodów ({totalHistory})</h2>
            </div>
            
            {history.length > 0 ? (
              <>
                <div className="history-list">
                  {history.map((item) => (
                    <div key={item.id} className="history-item" onClick={() => restoreAndPreviewFromHistory(item)} title="Kliknij, aby wczytać">
                      {item.image_base64 && (
                        <div className="history-thumb-wrapper">
                          <img src={`data:image/png;base64,${item.image_base64}`} alt="Thumb" className="history-thumb" />
                        </div>
                      )}
                      <div className="history-item-meta">
                        <span className={`type-tag ${item.code_type.toLowerCase()}`}>
                          {item.code_type === 'QR' ? 'QR' : item.barcode_type || 'BAR'}
                        </span>
                        <span className="history-item-date">
                          {new Date(item.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                        </span>
                      </div>
                      <div className="history-item-data">{item.data}</div>
                      <div className="history-item-colors">
                        <span className="color-dot" style={{ backgroundColor: item.fill_color }}></span>
                        <span className="color-dot" style={{ backgroundColor: item.back_color }}></span>
                      </div>
                    </div>
                  ))}
                </div>

                {totalHistory > limit && (
                  <div className="pagination-controls">
                    <button 
                      onClick={() => setSkip(skip - limit)} 
                      disabled={skip === 0}
                      className="btn-page"
                    >
                      ← Poprzednie
                    </button>
                    <span className="page-info">
                      Strona {Math.floor(skip / limit) + 1} z {Math.ceil(totalHistory / limit)}
                    </span>
                    <button 
                      onClick={() => setSkip(skip + limit)} 
                      disabled={skip + limit >= totalHistory}
                      className="btn-page"
                    >
                      Następne →
                    </button>
                  </div>
                )}
              </>
            ) : (
              <p className="no-history">Brak wpisów w historii.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App