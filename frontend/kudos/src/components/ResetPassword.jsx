import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { resetPassword } from "../api"; // Import API function
import "bootstrap/dist/css/bootstrap.min.css";

const ResetPassword = () => {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleResetPassword = async (e) => {
    e.preventDefault();
    let validationErrors = {};

    if (!oldPassword) validationErrors.oldPassword = "Old Password is required.";
    if (!newPassword) validationErrors.newPassword = "New Password is required.";
    if (!confirmPassword) validationErrors.confirmPassword = "Confirm Password is required.";
    if (newPassword !== confirmPassword) {
      validationErrors.confirmPassword = "Passwords do not match.";
    }

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      const refreshToken = localStorage.getItem("refreshToken"); // Get refresh token

      await resetPassword(oldPassword, newPassword, confirmPassword, refreshToken);
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      toast.success("Password reset successful! Please log in again.");
      navigate("/login");
    } catch (error) {
        if (error.response && error.response.data) {

            toast.error("Old Password is incorrect.");
          }
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center">Reset Password</h2>
      <form onSubmit={handleResetPassword} className="card p-4 shadow-sm mx-auto" style={{ maxWidth: "400px" }}>
        <div className="mb-3">
          <label className="form-label">Old Password</label>
          <input
            type="password"
            className={`form-control ${errors.oldPassword ? "is-invalid" : ""}`}
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
          />
          {errors.oldPassword && <div className="invalid-feedback">{errors.oldPassword}</div>}
        </div>

        <div className="mb-3">
          <label className="form-label">New Password</label>
          <input
            type="password"
            className={`form-control ${errors.newPassword ? "is-invalid" : ""}`}
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          {errors.newPassword && <div className="invalid-feedback">{errors.newPassword}</div>}
        </div>

        <div className="mb-3">
          <label className="form-label">Confirm New Password</label>
          <input
            type="password"
            className={`form-control ${errors.confirmPassword ? "is-invalid" : ""}`}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {errors.confirmPassword && <div className="invalid-feedback">{errors.confirmPassword}</div>}
        </div>

        <button type="submit" className="btn btn-primary w-100">Reset Password</button>
      </form>
    </div>
  );
};

export default ResetPassword;
