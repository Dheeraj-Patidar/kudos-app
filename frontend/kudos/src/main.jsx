import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import "bootstrap/dist/css/bootstrap.min.css"; 
import "react-toastify/dist/ReactToastify.css"; // Import Toastify styles
import { ToastContainer } from "react-toastify";


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <ToastContainer position="top-center" autoClose={3000} />
  </StrictMode>,
)
