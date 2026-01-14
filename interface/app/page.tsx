"use client";

import { useState } from "react";

export default function UltimatumTerminal() {
  const [input, setInput] = useState("");
  const [logs, setLogs] = useState<string[]>([
    "[SYSTEM] THE ULTIMATUM RESEARCH KERNEL INITIALIZED...",
    "[SYSTEM] WAITING FOR INPUT SEQUENCE...",
  ]);
  const [isLoading, setIsLoading] = useState(false);

  // This function connects the Interface (Face) to the Core (Brain)
  const runInference = async () => {
    if (!input.trim()) return;

    // Add user input to logs
    setLogs((prev) => [...prev, `> USER: ${input}`]);
    setIsLoading(true);

    try {
      // Connects to the backend server we will build next
      const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });

      const data = await response.json();
      setLogs((prev) => [...prev, `> ULTIMATUM: ${data.output}`]);
    } catch (error) {
      setLogs((prev) => [...prev, `[ERROR] CONNECTION REFUSED. IS CORE ACTIVE?`]);
    } finally {
      setIsLoading(false);
      setInput("");
    }
  };

  return (
    <main className="min-h-screen bg-black text-green-500 font-mono p-8 flex flex-col">
      {/* Header */}
      <header className="border-b border-green-800 pb-4 mb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold tracking-widest">THE ULTIMATUM</h1>
          <p className="text-xs text-green-800">ARCH: CAUSAL TRANSFORMER | V1.0</p>
        </div>
        <div className="flex gap-2 text-xs">
          <span className="px-2 py-1 border border-green-800 rounded">GPU: OFFLINE</span>
          <span className="px-2 py-1 border border-green-800 rounded animate-pulse">STATUS: IDLE</span>
        </div>
      </header>

      {/* Terminal Output Area */}
      <div className="flex-1 border border-green-900 rounded bg-gray-900/20 p-4 overflow-y-auto mb-4 shadow-[0_0_10px_rgba(0,255,0,0.1)]">
        {logs.map((log, i) => (
          <div key={i} className="mb-2 break-words">
            {log}
          </div>
        ))}
        {isLoading && <div className="animate-pulse">_ PROCESSING TENSORS...</div>}
      </div>

      {/* Command Input */}
      <div className="flex gap-4">
        <span className="py-3 text-xl">{">"}</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runInference()}
          placeholder="ENTER SEQUENCE..."
          className="flex-1 bg-transparent border-b border-green-800 focus:border-green-500 focus:outline-none py-3 text-lg"
        />
        <button
          onClick={runInference}
          className="px-6 py-2 border border-green-700 hover:bg-green-900 transition-colors uppercase text-sm tracking-wider"
        >
          EXECUTE
        </button>
      </div>
    </main>
  );
}