import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

const ForgotResetPassword = () => {
  const { uid, token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch(
        `http://localhost:8000/api/password-reset-confirm/${uid}/${token}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ new_password: password }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        toast.success("Password reset successful. Redirecting to login...");
        setTimeout(() => navigate("/login"), 2000);
      }
      if (data.token) {
        toast.error(data.token[0] || "Invalid or expired token.");
      } else if (data.new_password) {
        toast.error(data.new_password[0] || "Password validation error.");
      } else {
        toast.error("Something went wrong. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      setMessage("Failed to reset password.");
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow-lg">
            <div className="card-header bg-primary text-white text-center">
              <h3>Reset Password</h3>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <input className= "form-control"
                  type="password"
                  placeholder="Enter new password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <div className="mt-4">
                <button  className="btn btn-primary" type="submit">Reset Password</button>
                </div>
              </form>
              {message && <p>{message}</p>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotResetPassword;


























// import { useState } from "react";
// import { useSearchParams } from "react-router-dom";
// import { toast } from "react-toastify";
// import axios from "axios";

// const ForgotResetPassword = () => {
//   const [searchParams] = useSearchParams();
//   const email = searchParams.get("email");
//   const token = searchParams.get("token");

//   const [newPassword, setNewPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState("");

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (newPassword !== confirmPassword) {
//       toast.error("Passwords do not match.");
//       return;
//     }

//     try {
//       await axios.post("http://localhost:8000/api/password-reset-confirm/", {
//         email,
//         token,
//         new_password: newPassword,
//       });
//       toast.success("Password reset successful!");
//     } catch (error) {
//       toast.error("Failed to reset password.");
//     }
//   };

//   return (
//     <div className="container">
//       <h2>Reset Password</h2>
//       <form onSubmit={handleSubmit}>
//         <label>New Password:</label>
//         <input
//           type="password"
//           value={newPassword}
//           onChange={(e) => setNewPassword(e.target.value)}
//           required
//         />
//         <label>Confirm Password:</label>
//         <input
//           type="password"
//           value={confirmPassword}
//           onChange={(e) => setConfirmPassword(e.target.value)}
//           required
//         />
//         <button type="submit">Reset Password</button>
//       </form>
//     </div>
//   );
// };

// export default ForgotResetPassword;
