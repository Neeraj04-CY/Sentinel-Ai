import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Upload,
  Shield,
  AlertTriangle,
  CheckCircle,
  BarChart3,
  Zap,
  ChevronRight,
  Cpu,
  TrendingUp,
} from "lucide-react";

export default function SentinelAIUI() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  }, []);

  const riskConfig = {
    HIGH: { color: "text-red-500", bg: "bg-red-500/10", border: "border-red-500/20", icon: AlertTriangle },
    MEDIUM: { color: "text-amber-500", bg: "bg-amber-500/10", border: "border-amber-500/20", icon: AlertTriangle },
    LOW: { color: "text-emerald-500", bg: "bg-emerald-500/10", border: "border-emerald-500/20", icon: CheckCircle },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-black to-slate-950 text-white overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/5 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/3 rounded-full blur-3xl"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-10 px-8 py-6 border-b border-white/5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg">
              <Shield className="w-6 h-6" />
            </div>
            <span className="text-2xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              SentinelAI
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" className="text-slate-400 hover:text-white hover:bg-white/5">
              Dashboard
              <p className="text-slate-400 text-sm">
                (c) 2024 SentinelAI. Advanced Threat Intelligence Platform. All security protocols active.
              </p>
            </Button>
            <Button className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 rounded-full px-6">
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      <main className="relative z-10 px-8 py-12 max-w-7xl mx-auto">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-6">
            <Cpu className="w-4 h-4 mr-2 text-cyan-400" />
            <span className="text-sm font-medium text-cyan-400">Enterprise AI Security Platform</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
            <span className="bg-gradient-to-r from-white via-blue-100 to-cyan-100 bg-clip-text text-transparent">
              Threat Intelligence
            </span>
            <br />
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Redefined
            </span>
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto mb-10">
            Advanced AI-powered security analysis with real-time threat detection and predictive intelligence.
          </p>
        </motion.div>

        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="max-w-4xl mx-auto mb-16"
        >
          <Card className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl overflow-hidden">
            <CardContent className="p-0">
              <div className="p-8 border-b border-white/10">
                <div className="flex items-center mb-4">
                  <div className="p-3 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl mr-4">
                    <Upload className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">Security Analysis</h2>
                    <p className="text-slate-400">Upload your system logs for AI-powered threat detection</p>
                  </div>
                </div>
              </div>

              <div className="p-8">
                <div
                  className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
                    dragActive
                      ? "border-cyan-500 bg-cyan-500/5"
                      : "border-white/10 hover:border-cyan-500/50 hover:bg-white/5"
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent rounded-2xl"></div>
                  <div className="relative">
                    <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full flex items-center justify-center">
                      <Upload className="w-8 h-8 text-cyan-400" />
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Drop your CSV file here</h3>
                    <p className="text-slate-400 mb-6">or click to browse system files</p>
                    <input
                      type="file"
                      accept=".csv"
                      onChange={(e) => setFile(e.target.files[0])}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 rounded-full cursor-pointer transition-all hover:scale-105"
                    >
                      <Upload className="w-4 h-4 mr-2" />
                      Browse Files
                    </label>
                  </div>
                </div>

                {file && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    className="mt-6 p-4 bg-white/5 rounded-xl border border-white/10"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="p-2 bg-white/10 rounded-lg mr-4">
                          <BarChart3 className="w-5 h-5" />
                        </div>
                        <div>
                          <p className="font-medium">{file.name}</p>
                          <p className="text-sm text-slate-400">{(file.size / 1024).toFixed(2)} KB</p>
                        </div>
                      </div>
                      <Button
                        onClick={analyze}
                        disabled={loading}
                        className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 rounded-full px-8"
                      >
                        {loading ? (
                          <>
                            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                            Analyzing...
                          </>
                        ) : (
                          <>
                            Run Analysis <Zap className="w-4 h-4 ml-2" />
                          </>
                        )}
                      </Button>
                    </div>
                  </motion.div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Results Section */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="space-y-8"
            >
              {/* Risk Banner */}
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className={`p-6 rounded-2xl border ${riskConfig[result.risk_level].border} ${riskConfig[result.risk_level].bg} backdrop-blur-xl`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    {(() => {
                      const Icon = riskConfig[result.risk_level].icon;
                      return <Icon className={`w-8 h-8 mr-4 ${riskConfig[result.risk_level].color}`} />;
                    })()}
                    <div>
                      <p className="text-sm font-medium text-slate-400">Threat Level Identified</p>
                      <h2 className={`text-4xl font-bold ${riskConfig[result.risk_level].color}`}>
                        {result.risk_level}
                      </h2>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-400">Confidence Score</p>
                    <div className="flex items-center">
                      <TrendingUp className="w-5 h-5 text-emerald-500 mr-2" />
                      <span className="text-2xl font-bold">{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Insights Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* System Summary */}
                <Card className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-lg group-hover:scale-110 transition-transform">
                        <Cpu className="w-5 h-5 text-cyan-400" />
                      </div>
                      <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-cyan-400" />
                    </div>
                    <p className="text-sm font-medium text-slate-400 mb-2">System Insight</p>
                    <p className="text-lg font-semibold leading-snug">{result.system_summary}</p>
                  </CardContent>
                </Card>

                {/* Key Signals */}
                <Card className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-lg group-hover:scale-110 transition-transform">
                        <AlertTriangle className="w-5 h-5 text-pink-400" />
                      </div>
                      <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-pink-400" />
                    </div>
                    <p className="text-sm font-medium text-slate-400 mb-2">Key Signals</p>
                    <ul className="space-y-2">
                      {result.signals.slice(0, 3).map((s, i) => (
                        <li key={i} className="flex items-center text-sm">
                          <div className="w-1.5 h-1.5 bg-pink-500 rounded-full mr-3"></div>
                          {s}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                {/* Recommended Action */}
                <Card className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-gradient-to-br from-emerald-500/20 to-green-500/20 rounded-lg group-hover:scale-110 transition-transform">
                        <CheckCircle className="w-5 h-5 text-emerald-400" />
                      </div>
                      <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-400" />
                    </div>
                    <p className="text-sm font-medium text-slate-400 mb-2">Recommended Action</p>
                    <p className="text-lg font-semibold leading-snug">{result.recommended_action}</p>
                  </CardContent>
                </Card>

                {/* Confidence Meter */}
                <Card className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-6">
                      <div className="p-3 bg-gradient-to-br from-amber-500/20 to-yellow-500/20 rounded-lg group-hover:scale-110 transition-transform">
                        <BarChart3 className="w-5 h-5 text-amber-400" />
                      </div>
                      <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-amber-400" />
                    </div>
                    <p className="text-sm font-medium text-slate-400 mb-2">AI Confidence</p>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Accuracy</span>
                        <span className="font-bold">{(result.confidence * 100).toFixed(1)}%</span>
                      </div>
                      <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${result.confidence * 100}%` }}
                          transition={{ duration: 1, ease: "easeOut" }}
                          className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Detailed Analysis */}
              <Card className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden">
                <CardContent className="p-8">
                  <div className="flex items-center mb-6">
                    <div className="p-3 bg-gradient-to-br from-slate-500/20 to-slate-600/20 rounded-xl mr-4">
                      <Shield className="w-6 h-6 text-slate-300" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">Detailed Analysis</h3>
                      <p className="text-slate-400">Complete threat breakdown and security assessment</p>
                    </div>
                  </div>
                  <div className="p-6 bg-white/5 rounded-xl border border-white/10">
                    <p className="text-slate-300 leading-relaxed">{result.analysis}</p>
                    <div className="mt-6 pt-6 border-t border-white/10">
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center p-4 bg-white/5 rounded-lg">
                          <p className="text-sm text-slate-400">Severity</p>
                          <p className={`text-2xl font-bold ${riskConfig[result.risk_level].color}`}>
                            {result.risk_level}
                          </p>
                        </div>
                        <div className="text-center p-4 bg-white/5 rounded-lg">
                          <p className="text-sm text-slate-400">Files Scanned</p>
                          <p className="text-2xl font-bold">1</p>
                        </div>
                        <div className="text-center p-4 bg-white/5 rounded-lg">
                          <p className="text-sm text-slate-400">Threats Found</p>
                          <p className="text-2xl font-bold">{result.signals.length}</p>
                        </div>
                        <div className="text-center p-4 bg-white/5 rounded-lg">
                          <p className="text-sm text-slate-400">Response Time</p>
                          <p className="text-2xl font-bold">2.4s</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="relative z-10 px-8 py-8 mt-16 border-t border-white/5">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-slate-400 text-sm">
            (c) 2024 SentinelAI. Advanced Threat Intelligence Platform. All security protocols active.
          </p>
        </div>
      </footer>
    </div>
  );
}
