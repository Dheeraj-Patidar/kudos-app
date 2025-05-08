
import { useState } from "react";
import { toast } from "react-toastify";
const BASE_URL = import.meta.env.VITE_API_URL;
const ForgotPassword = () => {
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${BASE_URL}/password-reset/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      if (response.ok) {
        toast.success("Password reset link sent to your email.");
      } else {
        toast.error("Failed to send reset email.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card shadow-lg">
                        <div className="card-header bg-primary text-white text-center">
                            <h3>Forgot Password</h3>
                       </div>
                        <div className="card-body">
                            <form onSubmit={handleSubmit}>
                                <label className="form-label">Email:</label>
                                <input className= "form-control"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                 />
                                <div className="mt-4">
                                <button  className="btn btn-primary" type="submit">Send Reset Link</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>

  );
};

export default ForgotPassword;






















// import { useState } from "react";
// import { toast } from "react-toastify";
// import axios from "axios";

// const ForgotPassword = () => {
//     const [email, setEmail] = useState("");

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             await axios.post("http://localhost:8000/api/password-reset/", { email });
//             toast.success("Password reset link sent to your email.");
//         } catch (error) {
//             toast.error("Failed to send reset email.");
//         }
//     };

//     return (
//         <div className="container mt-5">
//             <div className="row justify-content-center">
//                 <div className="col-md-6">
//                     <div className="card shadow-lg">
//                         <div className="card-header bg-primary text-white text-center">
//                             <h3>Forgot Password</h3>
//                         </div>
//                         <div className="card-body">
//                             <form onSubmit={handleSubmit}>
//                                 <label className="form-label">Email:</label>
//                                 <input className= "form-control"
//                                     type="email"
//                                     value={email}
//                                     onChange={(e) => setEmail(e.target.value)}
//                                     required
//                                 />
//                                 <div className="mt-4">
//                                 <button  className="btn btn-primary" type="submit">Send Reset Link</button>
//                                 </div>
//                             </form>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default ForgotPassword;
