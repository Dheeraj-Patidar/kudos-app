import { Link } from "react-router-dom";
import { logout, getkudoscount} from "../Api";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
// import { useEffect, useState } from "react";

const Navbar = ({ kudosCount }) => {
  // const [kudoscount, setKudosCount] = useState(0)
  const isAuthenticated = localStorage.getItem("accessToken");
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      toast.success("Logout successful!");
      navigate("/login");
    } catch (error) {
      toast.error("Logout failed.");
      // navigate("/login");
    }
  };


  // useEffect(() => {
  //   const fetchKudosCount = async () => {
  //     try {
  //       const data = await getkudoscount(); // Call the API function
  //       setKudosCount(data.kudos_remaining); // Update state
  //     } catch (error) {
  //       console.error("Error fetching Kudos count:", error);
  //     }
  //   };

  //   fetchKudosCount();
  // }, []);

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
  <div className="container">
    <Link className="navbar-brand" to="/">Kudos App</Link>

    <button
      className="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarNav">
      <ul className="navbar-nav me-auto">
        <li className="nav-item">
          <Link className="nav-link" to="/">Home</Link>
        </li>

        {isAuthenticated && (
          <>
            <li className="nav-item">
              <Link className="nav-link" to="/kudos">Your Kudos</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/givekudos">Give Kudos</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/resetpassword">Reset Password</Link>
            </li>
          </>
        )}
      </ul>

      <ul className="navbar-nav ms-auto">
        {isAuthenticated ? (
          <>
            <li className="nav-item d-flex align-items-center me-2">
              <span className="text-white">Kudos Balance ({kudosCount})</span>
            </li>
            <li className="nav-item">
              <button className="btn btn-danger" onClick={handleLogout}>
                Logout
              </button>
            </li>
          </>
        ) : (
          <>
            <li className="nav-item">
              <Link className="nav-link" to="/login">Login</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/signup">Sign Up</Link>
            </li>
          </>
        )}
      </ul>
    </div>
  </div>
</nav>

  );
};

export default Navbar;
