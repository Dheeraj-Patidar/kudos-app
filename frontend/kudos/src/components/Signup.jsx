import { useState,useEffect } from "react";
import { signup } from "../Api";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import {getOrganizations} from "../Api";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [repassword, setRepassword] = useState("");
  const [organization, setOrganization] = useState("");
  const [organizations, setOrganizations] = useState([]);
  const [errors, setErrors] = useState({});

  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrganizations = async () => {
      try {
        const response = await getOrganizations();
        setOrganizations(response); // Store the list of organizations
      } catch (error) {
        console.error("Failed to fetch organizations:", error);
        toast.error("Failed to load organizations.");
      }
    };

    fetchOrganizations();
  }, []);
  const handleSignup = async (e) => {
    e.preventDefault();
    let validationErrors = {};

    if (!email) validationErrors.email = "Email is required.";
    if (!firstname) validationErrors.firstname = "First Name is required.";
    if (!lastname) validationErrors.lastname = "Last Name is required.";
    if (!password) validationErrors.password = "Password is required.";
    if (!repassword) validationErrors.repassword = "Confirm password is required.";
    if (password !== repassword) validationErrors.repassword = "Passwords do not match.";
    if (!organization) validationErrors.organization = "Organization is required.";
    if (password !== repassword) validationErrors.repassword = " Both Passwords do not match.";

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      await signup(email,firstname,lastname, password, repassword, organization);
      toast.success("Signup successful!");
      navigate("/login");
      setEmail("");
      setPassword("");
      setRepassword("");
      setOrganization("");
      setErrors({});
    } catch (error) {
      if (error.response && error.response.data) {
        setErrors(error.response.data); // Capture API errors like "Email already exists"
      } else {
        toast.error("Signup failed.");
      }
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow-lg">
            <div className="card-header bg-primary text-white text-center">
              <h3>Signup</h3>
            </div>
            <div className="card-body">
              <form onSubmit={handleSignup}>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className={`form-control ${errors.email ? "is-invalid" : ""}`}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}

                  />
                  {errors.email && <div className="invalid-feedback">{errors.email}</div>}
                </div>

                <div className="mb-3">
                  <label className="form-label">First Name</label>
                  <input
                    type="text"
                    className={`form-control ${errors.firstname ? "is-invalid" : ""}`}
                    value={firstname}
                    onChange={(e) => setFirstName(e.target.value)}

                  />
                  {errors.firstname && <div className="invalid-feedback">{errors.firstname}</div>}
                </div>

                <div className="mb-3">
                  <label className="form-label">Last Name</label>
                  <input
                    type="text"
                    className={`form-control ${errors.lastname ? "is-invalid" : ""}`}
                    value={lastname}
                    onChange={(e) => setLastName(e.target.value)}

                  />
                  {errors.lastname && <div className="invalid-feedback">{errors.lastname}</div>}
                </div>

                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className={`form-control ${errors.password ? "is-invalid" : ""}`}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}

                  />
                  {errors.password && <div className="invalid-feedback">{errors.password}</div>}
                </div>

                <div className="mb-3">
                  <label className="form-label">Confirm Password</label>
                  <input
                    type="password"
                    className={`form-control ${errors.repassword ? "is-invalid" : ""}`}
                    value={repassword}
                    onChange={(e) => setRepassword(e.target.value)}

                  />
                  {errors.repassword && <div className="invalid-feedback">{errors.repassword}</div>}
                </div>

                <div className="mb-3">
                  <label className="form-label">Organization</label>
                  <select
                    className={`form-control ${errors.organization ? "is-invalid" : ""}`}
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                  >
                    <option value="">Select an organization</option>
                    {organizations.map((org) => (
                      <option key={org.id} value={org.name}>
                        {org.name}
                      </option>
                    ))}
                  </select>
                  {errors.organization && <div className="invalid-feedback">{errors.organization}</div>}
                </div>

                <button type="submit" className="btn btn-primary w-100">Sign Up</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
