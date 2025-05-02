import { useState, useEffect } from "react";
import { getKudos, getLatestKudos } from "../Api";

const Home = () => {
    const [topUser, setTopUser] = useState(null);
    const [error, setError] = useState(null);
    const [kudos, setKudos] = useState([]);

    useEffect(() => {
        const fetchTopUser = async () => {
            try {
                const response = await getKudos();
                const kudos = response.data;

                //  Filter kudos from the last 7 days
                const now = new Date();
                const lastWeek = new Date();
                lastWeek.setDate(now.getDate() - 7);

                const kudosThisWeek = kudos.filter(kudo =>
                    new Date(kudo.timestamp) >= lastWeek
                );

                //  Count kudos per sender
                const userKudosCount = kudosThisWeek.reduce((acc, kudo) => {
                    const senderEmail = kudo.sender.email || "Unknown";
                    acc[senderEmail] = (acc[senderEmail] || 0) + 1;
                    return acc;
                }, {});

                //  Find user with max kudos
                const topUserEmail = Object.keys(userKudosCount).reduce((a, b) =>
                    userKudosCount[a] > userKudosCount[b] ? a : b, ""
                );

                setTopUser({ email: topUserEmail, count: userKudosCount[topUserEmail] || 0 });
            } catch (error) {
                console.error("Error fetching kudos:", error);
                setError("Failed to load top user.");
            }
        };

        fetchTopUser();
    }, []);


    useEffect(() => {
    const fetchlatestKudos = async () => {
        try{
            const response = await getLatestKudos();
            setKudos(response.data);

        }
        catch (error) {
            console.error("Error fetching kudos:", error);
            setError("Failed to load kudos.");
        }
    }
    fetchlatestKudos();
    }, []);

    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div className=" mt-4">
            <h2 className="text-center"> Top Kudos Giver To You This Week</h2>
            <div className="card p-4 shadow-sm mx-auto text-center" style={{ maxWidth: "400px" }}>
                {topUser ? (
                    <>
                        <h3 className="mb-3">{ topUser.email}</h3>
                        <p className="fw-bold text-success">{topUser.count} Kudos Given</p>
                    </>
                ) : (
                    <p className="text-muted">No kudos given this week</p>
                )}
            </div>

            <div className="latest-kudos mt-4">
            <h2 className="text-center"> Latest Kudos</h2>
            <div className="card p-4 shadow-sm mx-auto text-center" style={{ maxWidth: "400px" }}>
                {kudos ? (
                    <>
                    {kudos.map((kudo) => (
                        <div key={kudo.id} className="mb-3">
                            <h3>{kudo.sender.email}</h3>
                            <p>{kudo.message}</p>
                        </div>
                    ))
                    }
                    </>
                ) : (
                    <p className="text-muted">do not have any kudod</p>
                )}
            </div>
        </div>
        </div>

    );
};

export default Home;
