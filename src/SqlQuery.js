import React, { useState } from "react";

export default function SqlQuery() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    setLoading(true);
    setAnswer(null);
    setError(null);

    try {
      const response = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: query }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Unknown error");
      }

      const data = await response.json();
      setAnswer(data.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Ask SQL Query</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          placeholder="Enter natural language query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
          disabled={loading}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? "Loading..." : "Ask"}
        </button>
      </form>

      {loading && (
        <div style={styles.loading}>
          <div className="spinner" style={styles.spinner}></div>
          <p>Thinking...</p>
        </div>
      )}

      {answer !== null && !loading && (
        <p style={styles.answer}>Answer: {answer}</p>
      )}

      {error && <p style={styles.error}>Error: {error}</p>}

      {/* Inline CSS spinner */}
      <style>{`
        .spinner {
          margin: 10px auto;
          width: 30px;
          height: 30px;
          border: 4px solid #ddd;
          border-top-color: #4caf50;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 500,
    margin: "50px auto",
    padding: 20,
    border: "1px solid #ddd",
    borderRadius: 8,
    fontFamily: "Arial, sans-serif",
    textAlign: "center",
  },
  heading: {
    marginBottom: 20,
    color: "#333",
  },
  form: {
    display: "flex",
    gap: 10,
  },
  input: {
    flexGrow: 1,
    padding: 10,
    fontSize: 16,
    borderRadius: 4,
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 20px",
    backgroundColor: "#4caf50",
    color: "white",
    fontWeight: "bold",
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
  },
  loading: {
    marginTop: 20,
    color: "#4caf50",
    fontWeight: "bold",
  },
  spinner: {
    margin: "0 auto 10px",
  },
  answer: {
    marginTop: 20,
    fontSize: 18,
    fontWeight: "bold",
  },
  error: {
    marginTop: 20,
    color: "red",
  },
};
