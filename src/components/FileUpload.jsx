import React, { useState } from 'react';

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  // Handles file selection from the input
  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setMessage(`Selected: ${event.target.files[0].name}`);
    } else {
      setSelectedFile(null);
      setMessage('No file selected.');
    }
  };

  // Handles the upload process
  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first!');
      return;
    }

    setIsUploading(true);
    setMessage('Uploading...');

    const formData = new FormData();
    formData.append('file', selectedFile); // 'file' must match the backend's expected field name

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Upload successful! ${data.message}`);
        setSelectedFile(null); // Clear selected file after successful upload
        // You might want to clear the input field too if desired
        document.getElementById('file-input').value = ''; 
      } else {
        setMessage(`Upload failed: ${data.detail || 'Unknown error'}`);
        console.error('Upload error response:', data);
      }
    } catch (error) {
      setMessage(`Network error: ${error.message}`);
      console.error('Network error during upload:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px', margin: '20px' }}>
      <h2>Upload Document for Search</h2>
      <input 
        type="file" 
        id="file-input" // Added an ID for clearing the input if needed
        onChange={handleFileChange} 
        disabled={isUploading} 
      />
      <button 
        onClick={handleUpload} 
        disabled={!selectedFile || isUploading} 
        style={{ marginLeft: '10px', padding: '8px 15px', cursor: 'pointer' }}
      >
        {isUploading ? 'Uploading...' : 'Upload File'}
      </button>
      {message && <p style={{ marginTop: '10px', color: message.includes('failed') || message.includes('error') ? 'red' : 'green' }}>{message}</p>}
    </div>
  );
}

export default FileUpload; 