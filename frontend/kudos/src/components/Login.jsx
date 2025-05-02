import { useState } from "react";
import { login, getkudoscount } from "../Api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
const Login =({setKudosCount})=>{
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        let validationErrors = {};

        if (!email) validationErrors.email = "Email is required.";
        if (!password) validationErrors.password = "Password is required.";

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            return;
        }

        try {
            const response = await login(email, password);
            localStorage.setItem("accessToken",response.data.access);
            localStorage.setItem("refreshToken",response.data.refresh);
            const updatedKudosCount = await getkudoscount();
            setKudosCount(updatedKudosCount.kudos_remaining);
            toast.success("Login successful!");
            navigate("/");
            setEmail("");
            setPassword("");
            setErrors({});
        } catch (error) {
            // console.error("Full error object:", error);
            toast.error(error.response.data.detail);
    }


    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card shadow-lg">
                        <div className="card-header bg-primary text-white text-center">
                            <h3>Login</h3>
                        </div>
                        <div className="card-body">

                            <form onSubmit={handleLogin}>
                                <div className="mb-3">
                                    <label className="form-label">Email</label>
                                    <input
                                        type="email"
                                        className={`form-control ${errors.email && "is-invalid"}`}
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                    />
                                    <div className="invalid-feedback">{errors.email}</div>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input
                                        type="password"
                                        className={`form-control ${errors.password && "is-invalid"}`}
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                    <div className="invalid-feedback">{errors.password}</div>
                                </div>
                                <button type="submit" className="btn btn-primary">
                                    Login
                                </button>
                                <Link to="/forgot-password" className="float-end">
                                    Forgot Password?
                                </Link>

                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login
