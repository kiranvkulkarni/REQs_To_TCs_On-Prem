import React, { useState } from 'react';
import axios from 'axios';

interface ExportResult {
  message: string;
  exported_files: number;
}

const Export: React.FC = () => {
  const [result, setResult] = useState<ExportResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExport = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/v1/export');
      setResult(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Export Accepted Test Cases</h1>
      <p className="mb-4">Export all accepted test cases to .feature files.</p>
      <button
        onClick={handleExport}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? "Exporting..." : "Export to .feature files"}
      </button>
      {result && (
        <div className="mt-4 p-4 bg-green-100 dark:bg-green-900 rounded">
          <h3 className="font-bold">Export Successful</h3>
          <p>{result.message}</p>
          <p>Exported {result.exported_files} files.</p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 rounded">
          <h3 className="font-bold">Export Failed</h3>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default Export;