import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import './App.css'
import Signup from "./components/Signup";
import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Home from "./components/Home";
import ResetPassword from "./components/ResetPassword";
import PrivateRoute from "./components/PrivateRoute";
import GiveKudos from "./components/GiveKudos";
import Kudos from "./components/Kudos";
import ForgotPassword from "./components/ForgotPassword";
import ForgotResetPassword from "./components/ForgotResetPassword";
import { getkudoscount } from "./Api"; // Import the API call
import { useState,useEffect } from "react";

function App() {

  const [kudosCount, setKudosCount] = useState(0);

  useEffect(() => {
    const fetchKudosCount = async () => {
      try {
        const response = await getkudoscount();
        setKudosCount(response.kudos_remaining);
      } catch (error) {
        console.error("Error fetching Kudos count:", error);
      }
    };
    fetchKudosCount();
  }, []);

  return (
    <>

    <Router>
    <Navbar kudosCount={kudosCount}/>
      <Routes>
        <Route path="/" element={<PrivateRoute> <Home/> </PrivateRoute>} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/login" element={<Login setKudosCount={setKudosCount}/>}/>
        <Route path="/givekudos" element={<GiveKudos setKudosCount={setKudosCount}/>}/>
        <Route path="/kudos" element={<Kudos/>} />
        <Route path="/resetpassword" element={<ResetPassword/>} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token" element={<ForgotResetPassword />} />
      </Routes>
    </Router>
    </>
  )
}

export default App
