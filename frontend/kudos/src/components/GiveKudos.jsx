import { useState } from "react";
import { giveKudos } from "../api";
import { toast } from "react-toastify";
import { useEffect } from "react";
import { getUser,getkudoscount} from "../api";

const GiveKudos = ({ setKudosCount }) => {
    const [receiver, setReceiver] = useState("");
    const [receivers, setReceivers] = useState([]);
    const [message, setMessage] = useState("");
    const [errors, setErrors] = useState({});

    useEffect(() => {
        const fetchReceivers = async () => {
            try {
                const response = await getUser();
                setReceivers(response.data);
            } catch (error) {
                console.error("Failed to fetch receivers:", error);
                toast.error("Failed to load receivers.");
            }
        };
        fetchReceivers();
    }, []);

    const handleGiveKudos = async (e) => {
        e.preventDefault();
        let validationErrors = {};

        if (!receiver) validationErrors.receiver = "Receiver is required.";
        if (!message) validationErrors.message = "Message is required.";

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            return;
        }

        try {
            await giveKudos(receiver, message);
            const updatedKudosCount = await getkudoscount();
            setKudosCount(updatedKudosCount.kudos_remaining);
            toast.success("Kudos sent successfully!");
            setReceiver("");
            setMessage("");
            setErrors({});
        } catch (error) {
            if (error.response && error.response.data) {
                console.error("Error response:", error.response.data);

                const backendErrors = error.response.data;

                // Handle receiver-related errors (e.g., user not found)
                if (backendErrors.receiver) {
                    validationErrors.receiver = backendErrors.receiver;
                }

                // Handle general errors (e.g., no kudos left, rate limit)
                if (backendErrors.non_field_errors) {
                    backendErrors.non_field_errors.forEach((err) => toast.error(err));
                }

                // Preserve all validation errors
                setErrors(validationErrors);
            } else {
                console.error("Unexpected error:", error);
                toast.error("An unexpected error occurred.");
            }
        }
    };


    return(
        <div className="container mt-4">
            <h2 className="text-center">Give Kudos</h2>
            <form onSubmit={handleGiveKudos} className="card p-4 shadow-sm mx-auto" style={{ maxWidth: "400px" }}>
                <div className="mb-3">
                    <label className="form-label">Receiver</label>
                    <select
                    className={`form-control ${errors.receiver ? "is-invalid" : ""}`}
                    value={receiver}
                    onChange={(e) => setReceiver(e.target.value)}
                  >
                    <option value="">Select Receiver</option>
                    {receivers.map((receiver) => (
                      <option key={receiver.id} value={receiver.email}>
                        {receiver.email}
                      </option>
                    ))}
                  </select>
                    {errors.receiver && <div className="invalid-feedback">{errors.receiver}</div>}
                </div>

                <div className="mb-3">
                    <label className="form-label">Message</label>
                    <textarea
                        className={`form-control ${errors.message ? "is-invalid" : ""}`}
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                    ></textarea>
                    {errors.message && <div className="invalid-feedback">{errors.message}</div>}
                </div>

                <button type="submit" className="btn btn-primary">Send Kudos</button>
            </form>
        </div>
    )
}

export default GiveKudos;
