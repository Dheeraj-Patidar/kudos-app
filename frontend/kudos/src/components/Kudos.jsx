import { useState, useEffect } from "react";
import { getKudos } from "../Api";

const Kudos = () => {
    const [kudos, setKudos] = useState([]);
    const [filter, setFilter] = useState("all");

    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchKudos = async () => {
            try {
                const response = await getKudos();
                setKudos(response.data);
            } catch (error) {
                console.error("Error fetching kudos:", error);
                setError("Failed to load kudos.");
            }
        };

        fetchKudos();
    }, []);

    //  Function to filter kudos based on date range
    const getFilteredKudos = () => {
        if (filter === "all") return kudos;

        const now = new Date();
        return kudos.filter((kudo) => {
            const kudoDate = new Date(kudo.timestamp);

            if (filter === "week") {
                const lastWeek = new Date();
                lastWeek.setDate(now.getDate() - 7);
                return kudoDate >= lastWeek;
            }

            if (filter === "month") {
                const lastMonth = new Date();
                lastMonth.setMonth(now.getMonth() - 1);
                return kudoDate >= lastMonth;
            }

            return true;
        });
    };

    const filteredKudos = getFilteredKudos();

    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div className="container mt-4">
            <h2 className="text-center">Your Kudos</h2>

            {/* Dropdown to select filter */}
            <div className="mb-3 text-center">
                <label htmlFor="filter" className="me-2">Filter:</label>
                <select id="filter" value={filter} onChange={(e) => setFilter(e.target.value)}>
                    <option value="all">All</option>
                    <option value="week">Last Week</option>
                    <option value="month">Last Month</option>
                </select>
            </div>

            <div className="card p-4 shadow-sm mx-auto" style={{ maxWidth: "400px" }}>
                <ul className="list-group list-group-flush">
                    <li className="list-group-item d-flex justify-content-between align-items-center fw-bold">
                        Given By <span>Kudos</span>
                    </li>

                    {filteredKudos.length > 0 ? (
                        filteredKudos.map((kudo, index) => (
                            <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                                {kudo.sender.email || "Unknown Sender"}
                                <span className="badge bg-primary rounded-pill">{kudo.message}</span>
                            </li>
                        ))
                    ) : (
                        <li className="list-group-item text-center text-muted">No kudos found</li>
                    )}
                </ul>
            </div>
        </div>
    );
};

export default Kudos;
