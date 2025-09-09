import { useState } from "react";
import "./App.css";

const API_BASE =
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

function App() {
  const [health, setHealth] = useState(null);
  const [backends, setBackends] = useState(null);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null);

  async function fetchJSON(path) {
    setError(null);
    const url = `${API_BASE}${path}`;
    const res = await fetch(url, { headers: { Accept: "application/json" } });
    if (!res.ok) {
      let msg = res.statusText;
      try {
        const j = await res.json();
        msg = j?.message || JSON.stringify(j);
      } catch (_) {}
      throw new Error(`${res.status} ${msg}`);
    }
    return res.json();
  }

  async function fetchHealth() {
    try {
      setLoading("health");
      const data = await fetchJSON("/api/health");
      setHealth(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(null);
    }
  }

  async function fetchBackends() {
    try {
      setLoading("backends");
      const data = await fetchJSON("/api/backends");
      setBackends(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="space-y-6">
          <div className="flex justify-between space-x-4">
            <button
              onClick={fetchHealth}
              className="hover:bg-red-500 p-4 transition-all rounded-md"
              disabled={loading === "health"}
            >
              {loading === "health" ? "Checking..." : "Check health"}
            </button>
            <button
              onClick={fetchBackends}
              className="hover:bg-red-500 p-4 transition-all rounded-md"
              disabled={loading === "backends"}
            >
              {loading === "backends" ? "Loading..." : "List backends"}
            </button>
          </div>

          <div className="h-60 bg-white overflow-auto p-4 text-left text-black rounded">
            {error && (
              <div className="mb-3 text-red-600">
                Error: {error}
              </div>
            )}

            {!error && !health && !backends && (
              <div className="text-gray-500">Click a button to fetch data…</div>
            )}

            {health && (
              <>
                <h3 className="font-bold mb-2">Health</h3>
                <pre className="text-sm">
                  {JSON.stringify(health, null, 2)}
                </pre>
              </>
            )}

            {backends && (
              <>
                <h3 className="font-bold mt-4 mb-2">Backends</h3>
                <pre className="text-sm">
                  {JSON.stringify(backends, null, 2)}
                </pre>
              </>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
