import { useState } from "react";
import axios from "axios";

function App() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);

    const runQuery = async () => {
        try {
            console.log("Here is the query", query);
            const response = await axios.post("http://34.205.24.189/query", { query });
            setResults(response.data.results);
        } catch (error) {
            console.error("Query failed", error);
        }
    };

    return (
        <div className="container">
            <h1>Athena Query UI</h1>
            <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your SQL query"
                rows="5"
                cols="50"
            />
            <button onClick={runQuery}>Run Query</button>

            {results.length > 0 && (
                <table border="1">
                    <thead>
                        <tr>
                            {results[0].map((col, index) => (
                                <th key={index}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {results.slice(1).map((row, rowIndex) => (
                            <tr key={rowIndex}>
                                {row.map((col, colIndex) => (
                                    <td key={colIndex}>{col}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default App;
