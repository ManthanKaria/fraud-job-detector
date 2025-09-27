"use client";

import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

import ReactSpeedometer from "react-d3-speedometer";

export default function Home() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const resultRef = useRef(null);

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [result]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: text }), 
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const { fraudulent, confidence, cleaned_text } = await response.json();
      setResult({ fraudulent, confidence, cleaned_text });
    } catch (err) {
      console.error(err);
      setResult({ error: "Something went wrong. Try again!" });
    } finally {
      setLoading(false);
    }
  };


  // Helper: convert confidence (0–1) → percent (0–100)
  const confPercent = result ? Math.round(result.confidence * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-900 to-blue-800 text-white font-sans flex flex-col items-center px-6 py-10">
      {/* Hero */}
      <motion.div
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="mt-20 text-center max-w-2xl"
      >
        <h1 className="text-5xl font-bold mb-4 text-gradient bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-600 tracking-wide">
          Fraud Job Posting Detector
        </h1>
        <p className="text-lg text-gray-200">
          Paste a job description and let AI detect if it’s real or fake.
        </p>
      </motion.div>

      {/* Form */}
      <motion.form
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        onSubmit={handleSubmit}
        className="mt-12 w-full max-w-2xl"
      >
        <Card className="bg-white/10 border border-white/20 rounded-2xl shadow-xl backdrop-blur-lg">
          <CardContent className="p-8">
            <Textarea
              placeholder="Paste job description here..."
              className="w-full text-white bg-black/20 border border-white/40 focus:ring-2 focus:ring-cyan-500 rounded-xl mb-6 placeholder-white"
              rows={6}
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <Button
              type="submit"
              disabled={loading}
              className="w-full py-4 text-lg font-medium rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 text-white hover:bg-gradient-to-l hover:from-indigo-600 hover:to-cyan-500 transition-all duration-300"
            >
              {loading ? "Analyzing..." : "Detect Fraud"}
            </Button>
          </CardContent>
        </Card>
      </motion.form>

      {/* Result & Gauge */}
      {result && (
        <motion.div
          ref={resultRef}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="mt-12 w-full max-w-2xl"
        >
          <Card className="bg-white/10 border border-white/20 rounded-2xl shadow-xl backdrop-blur-lg">
            <CardContent className="p-8 text-center">
              {result.error ? (
                <p className="text-red-400 font-semibold">{result.error}</p>
              ) : (
                <>
                  <h2 className="text-2xl font-semibold mb-4 text-gradient bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-600">
                    Prediction Result
                  </h2>

                  {/* The Speedometer / Gauge */}
                  <div className="mx-auto" style={{ width: 300, height: 160 }}>
                    <ReactSpeedometer
                      value={confPercent}
                      maxValue={100}
                      needleColor="#000"
                      segments={3}
                      segmentColors={["#ff4d4f", "#fbc02d", "#4caf50"]}
                      ringWidth={20}
                      customSegmentStops={[0, 30, 70, 100]} // Adjusts "Medium" center arc
                      currentValueText=""
                      needleTransitionDuration={1000}
                      needleTransition="easeElastic"
                      labelFontSize="11px"
                      customSegmentLabels={[
                        {
                          text: "Low",
                          position: "OUTSIDE",
                          color: "#fff",
                          fontSize: "12px",
                        },
                        {
                          text: "Medium",
                          position: "OUTSIDE",
                          color: "#fff",
                          fontSize: "12px",
                          fontFamily: "Arial", // Helps avoid italic distortions
                        },
                        {
                          text: "High",
                          position: "OUTSIDE",
                          color: "#fff",
                          fontSize: "12px",
                        },
                      ]}
                    />


                  </div>

                  {/* Fraud / Legit Text */}
                  <p className="text-xl font-semibold mt-4">
                    {result.fraudulent ? "🚨 Fraudulent" : "✅ Legitimate"}
                  </p>
                  <motion.p
                    className="mt-4 text-2xl font-bold text-white drop-shadow-md"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                  >
                    Confidence: <span className="text-cyan-300">{confPercent}%</span>
                  </motion.p>
                </>
              )}
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Footer */}
      <footer className="mt-20 mb-6 text-sm text-gray-300">
        Made with ❤️ by Manthan |
      // {" "}
        // <a
        //   href="https://your-resume-link.com"
        //   className="underline text-cyan-400 hover:text-cyan-500"
        // >
        //   Resume
        // </a>{" "}
        |{" "}
        <a
          href="https://github.com/ManthanKaria"
          className="underline text-cyan-400 hover:text-cyan-500"
        >
          GitHub
        </a>
      </footer>
    </div>
  );
}
