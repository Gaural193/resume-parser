import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileType, FolderArchive } from 'lucide-react';

export default function FileUpload({ onFilesSelected, isUploading }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onFilesSelected(acceptedFiles);
    }
  }, [onFilesSelected]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    // We don't restrict to just .zip because they might drop a folder of PDFs.
    // Accept standard document types + zip
    accept: {
      'application/zip': ['.zip'],
      'application/x-zip-compressed': ['.zip'],
      'application/x-zip': ['.zip'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    }
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div 
        {...getRootProps()} 
        className={`relative overflow-hidden rounded-2xl border-2 border-dashed transition-all duration-300 ease-in-out
          ${isDragActive ? 'border-brand-500 bg-brand-50 shadow-inner' : 'border-slate-300 bg-white hover:border-brand-400 hover:bg-slate-50'}
          ${isUploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
      >
        <input {...getInputProps()} disabled={isUploading} />
        
        {/* We use webkitdirectory to allow folder selection via click if the user prefers that over drag-drop */}
        <input 
            type="file" 
            webkitdirectory="true" 
            className="hidden" 
            id="folder-upload" 
            onChange={(e) => {
                if (e.target.files.length > 0) {
                    onFilesSelected(Array.from(e.target.files));
                }
                e.target.value = null;
            }}
            disabled={isUploading}
        />
        
        <div className="p-12 text-center flex flex-col items-center space-y-4">
          <div className="p-4 bg-brand-100 rounded-full text-brand-600 mb-2 shadow-sm">
             <UploadCloud size={40} />
          </div>
          
          <h3 className="text-xl font-semibold text-slate-800">
            {isDragActive ? 'Drop your files here!' : 'Upload Resumes'}
          </h3>
          
          <p className="text-slate-500 max-w-sm">
            Drag and drop a <strong>ZIP file</strong> or a <strong>Folder</strong> containing PDF and DOCX files.
          </p>
          
          <div className="flex gap-4 mt-6">
             <div className="flex items-center text-sm text-slate-400 bg-slate-100 px-3 py-1.5 rounded-full">
               <FolderArchive size={16} className="mr-2" /> ZIP Archive
             </div>
             <div className="flex items-center text-sm text-slate-400 bg-slate-100 px-3 py-1.5 rounded-full">
               <FileType size={16} className="mr-2" /> PDF & DOCX
             </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-slate-100 w-full flex justify-center">
             <button 
                type="button"
                className="btn-primary"
                onClick={(e) => {
                    e.stopPropagation();
                    document.getElementById('folder-upload').click();
                }}
                disabled={isUploading}
             >
                Or select a Folder
             </button>
          </div>
        </div>
      </div>
    </div>
  );
}
