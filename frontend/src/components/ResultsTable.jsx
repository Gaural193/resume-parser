import React from 'react';
import { Download, FileText, CheckCircle, AlertTriangle } from 'lucide-react';
import Papa from 'papaparse';

export default function ResultsTable({ data }) {
  if (!data) return null;

  const { results, errors, total_processed, successful, failed } = data;

  const handleDownloadCSV = () => {
    if (!results || results.length === 0) return;
    
    // Map data to the desired CSV format
    const csvData = results.map(row => ({
      'Name': row.name || '',
      'Email': row.email || '',
      'Phone': row.phone || '',
      'Location': row.location || '',
      'File Name': row.file_name || ''
    }));

    const csv = Papa.unparse(csvData);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `parsed_resumes_${new Date().getTime()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="glass-panel p-4 flex items-center justify-between border-l-4 border-l-blue-500">
           <div>
             <p className="text-sm text-slate-500 font-medium">Total Processed</p>
             <p className="text-2xl font-bold text-slate-800">{total_processed}</p>
           </div>
           <FileText className="text-blue-200" size={32} />
        </div>
        <div className="glass-panel p-4 flex items-center justify-between border-l-4 border-l-emerald-500">
           <div>
             <p className="text-sm text-slate-500 font-medium">Successful</p>
             <p className="text-2xl font-bold text-slate-800">{successful}</p>
           </div>
           <CheckCircle className="text-emerald-200" size={32} />
        </div>
        <div className="glass-panel p-4 flex items-center justify-between border-l-4 border-l-rose-500">
           <div>
             <p className="text-sm text-slate-500 font-medium">Failed</p>
             <p className="text-2xl font-bold text-slate-800">{failed}</p>
           </div>
           <AlertTriangle className="text-rose-200" size={32} />
        </div>
      </div>

      <div className="glass-panel overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-white/50">
          <h2 className="text-lg font-semibold text-slate-800">Extracted Candidates</h2>
          <button 
            onClick={handleDownloadCSV}
            className="btn-primary flex items-center shadow-brand-500/20"
            disabled={results.length === 0}
          >
            <Download size={18} className="mr-2" />
            Download CSV
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-sm">
                <th className="p-4 font-medium border-b border-slate-200">Name</th>
                <th className="p-4 font-medium border-b border-slate-200">Email</th>
                <th className="p-4 font-medium border-b border-slate-200">Phone</th>
                <th className="p-4 font-medium border-b border-slate-200">Location</th>
                <th className="p-4 font-medium border-b border-slate-200">File Name</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {results.length === 0 ? (
                <tr>
                  <td colSpan="5" className="p-8 text-center text-slate-400">
                    No successful parses to display.
                  </td>
                </tr>
              ) : (
                results.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4 text-slate-800 font-medium">{row.name || '-'}</td>
                    <td className="p-4 text-slate-600">{row.email || '-'}</td>
                    <td className="p-4 text-slate-600">{row.phone || '-'}</td>
                    <td className="p-4 text-slate-600">{row.location || '-'}</td>
                    <td className="p-4 text-slate-400 text-sm max-w-[200px] truncate" title={row.file_name}>{row.file_name}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {errors && errors.length > 0 && (
        <div className="mt-6 glass-panel border-l-4 border-l-rose-500 overflow-hidden">
          <div className="p-4 bg-rose-50 border-b border-rose-100 flex items-center">
            <AlertTriangle className="text-rose-500 mr-2" size={20} />
            <h3 className="font-semibold text-rose-800">Errors ({errors.length})</h3>
          </div>
          <ul className="p-4 max-h-48 overflow-y-auto text-sm text-slate-600 space-y-1">
            {errors.map((err, idx) => (
              <li key={idx} className="flex items-start">
                <span className="mr-2 mt-1 w-1.5 h-1.5 rounded-full bg-rose-400 shrink-0"></span>
                {err}
              </li>
            ))}
          </ul>
        </div>
      )}
      
    </div>
  );
}
