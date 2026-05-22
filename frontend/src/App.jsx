import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultsTable from './components/ResultsTable';
import { uploadFiles } from './api';
import { Briefcase, Loader2 } from 'lucide-react';

function App() {
  const [isUploading, setIsUploading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleFilesSelected = async (files) => {
    setIsUploading(true);
    setError(null);
    setData(null);

    try {
      const responseData = await uploadFiles(files);
      setData(responseData);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'An error occurred during processing.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-brand-200 selection:text-brand-900 pb-20">
      
      {/* Header */}
      <header className="bg-white/70 backdrop-blur-md border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-brand-500 text-white p-2 rounded-lg shadow-sm">
              <Briefcase size={24} />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600">
              Resume Parser
            </h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-12">
        <div className="text-center mb-10">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-800 tracking-tight mb-4">
            Automate your candidate pipeline
          </h2>
          <p className="text-lg text-slate-500 max-w-2xl mx-auto">
            Upload your ZIP files or directories containing resumes. Our NLP engine will extract contact info and locations, delivering ready-to-use CSV data.
          </p>
        </div>

        {/* Upload Zone */}
        <FileUpload onFilesSelected={handleFilesSelected} isUploading={isUploading} />

        {/* Error Message */}
        {error && (
          <div className="max-w-2xl mx-auto mt-6 p-4 bg-rose-50 text-rose-700 rounded-xl border border-rose-200 flex items-start shadow-sm">
             <div className="mr-3 mt-0.5 font-bold">Error:</div>
             <div>{error}</div>
          </div>
        )}

        {/* Loading State */}
        {isUploading && (
          <div className="max-w-2xl mx-auto mt-12 p-12 flex flex-col items-center justify-center glass-panel">
            <Loader2 className="animate-spin text-brand-500 mb-4" size={48} />
            <h3 className="text-xl font-medium text-slate-700">Processing Resumes...</h3>
            <p className="text-slate-500 mt-2 text-center max-w-sm">
              We are extracting text, names, emails, and locations. This may take a few moments for large batches.
            </p>
          </div>
        )}

        {/* Results */}
        {!isUploading && data && (
          <ResultsTable data={data} />
        )}
      </main>

    </div>
  );
}

export default App;
