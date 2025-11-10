(function () {
  // Use global React/ReactDOM provided by UMD scripts
  const { useState, useEffect } = React;

  // Prefer explicit local API unless user overrides via localStorage
  const DEFAULT_API_BASE = "http://127.0.0.1:8787";
  const API_BASE = (function () {
    try {
      return localStorage.getItem("API_BASE") || DEFAULT_API_BASE;
    } catch {
      return DEFAULT_API_BASE;
    }
  })();

  function App() {
    const [ticker, setTicker] = useState("BBAS3.SA");
    const [prompt, setPrompt] = useState(
      "Full deep-dive with catalysts, risks and valuation hooks."
    );
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState("");
    const [error, setError] = useState("");
    const [health, setHealth] = useState("");

    useEffect(() => {
      // Quick health check for visibility
      fetch(`${API_BASE}/v1/health`, { cache: "no-store" })
        .then((r) => (r.ok ? r.json() : Promise.reject(r.statusText)))
        .then((j) =>
          setHealth(j.ok ? "✅ API reachable" : "⚠️ Health check failed")
        )
        .catch(() =>
          setHealth("⚠️ Cannot reach API. Check port/CORS/firewall.")
        );
    }, []);

    async function onSubmit(e) {
      e.preventDefault();
      setLoading(true);
      setError("");
      setResult("");
      try {
        const res = await fetch(`${API_BASE}/v1/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ticker, prompt }),
        });
        const text = await res.text();
        if (!res.ok) {
          throw new Error(text || `HTTP ${res.status}`);
        }
        // Try parse JSON then render markdown/plain
        let payload;
        try {
          payload = JSON.parse(text);
        } catch {
          payload = { content_markdown: text };
        }
        setResult(payload.content_markdown || text || "(no content)");
      } catch (err) {
        setError(String(err));
      } finally {
        setLoading(false);
      }
    }

    // Simple markdown rendering if marked is available; else show as <pre>
    function RenderMarkdown({ content }) {
      if (window.marked && typeof window.marked.parse === "function") {
        return React.createElement("div", {
          className: "card prose prose-invert",
          dangerouslySetInnerHTML: {
            __html: window.marked.parse(content || ""),
          },
        });
      }
      return React.createElement("pre", { className: "card" }, content || "");
    }

    return React.createElement(
      "div",
      { className: "container" },
      React.createElement("h1", null, "Agno Finance Agents"),
      React.createElement(
        "p",
        null,
        "Django + React (UMD) UI backed by FastAPI + Agno team."
      ),
      React.createElement(
        "div",
        { className: "footer" },
        "API base: ",
        API_BASE,
        " — change via ",
        React.createElement(
          "code",
          null,
          'localStorage.setItem("API_BASE","http://127.0.0.1:8787")'
        )
      ),
      React.createElement(
        "div",
        { className: "footer", style: { marginTop: 6 } },
        "Health: ",
        health
      ),

      React.createElement(
        "form",
        { onSubmit },
        React.createElement("input", {
          value: ticker,
          onChange: (e) => setTicker(e.target.value),
          placeholder: "Ticker e.g. AAPL or BBAS3.SA",
        }),
        React.createElement("textarea", {
          rows: 4,
          value: prompt,
          onChange: (e) => setPrompt(e.target.value),
          placeholder: "Your analysis goal...",
        }),
        React.createElement(
          "button",
          { disabled: loading },
          loading ? "Analyzing..." : "Run Analysis"
        )
      ),

      error
        ? React.createElement("div", { className: "card" }, "⚠️ ", error)
        : null,
      result ? React.createElement(RenderMarkdown, { content: result }) : null
    );
  }

  function onSubmit(e) {
    return App.prototype.onSubmit ? App.prototype.onSubmit(e) : null;
  } // no-op to appease lints

  // Mount
  const rootEl = document.getElementById("root");
  if (!rootEl) {
    document.body.innerHTML +=
      '<div style="color:#fff;padding:16px">Root element not found.</div>';
  } else {
    ReactDOM.createRoot(rootEl).render(React.createElement(App));
  }
})();
