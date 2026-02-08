import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

interface Screenshot {
  id: number;
  filename: string;
  feature_name: string;
  status: string; // "pending", "generated", "accepted", "rejected"
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [screenshots, setScreenshots] = useState<Screenshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchScreenshots = async () => {
      try {
        await axios.get('/api/v1/ingest'); // Dummy call to trigger ingest if needed
        await axios.get('/api/v1/generate'); // Generate if not done
        const screenshotsRes = await axios.get('/api/v1/export'); // Get all for dashboard
        setScreenshots(screenshotsRes.data.results || []);
        setLoading(false);
      } catch (err: any) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchScreenshots();
  }, []);

  if (loading) return <div className="text-center p-8">Loading...</div>;
  if (error) return <div className="text-center p-8 text-red-500">Error: {error}</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {screenshots.map((screenshot) => (
          <div
            key={screenshot.id}
            className={`p-4 rounded shadow-md ${
              screenshot.status === 'accepted'
                ? 'bg-green-100 dark:bg-green-900'
                : screenshot.status === 'rejected'
                ? 'bg-red-100 dark:bg-red-900'
                : screenshot.status === 'generated'
                ? 'bg-yellow-100 dark:bg-yellow-900'
                : 'bg-blue-100 dark:bg-blue-900'
            }`}
          >
            <h2 className="font-bold">{screenshot.feature_name}</h2>
            <p className="text-sm text-gray-500">File: {screenshot.filename}</p>
            <p className="text-sm text-gray-500">Status: {screenshot.status}</p>
            <p className="text-sm text-gray-500">Created: {new Date(screenshot.created_at).toLocaleString()}</p>
            <Link
              to={`/review/${screenshot.id}`}
              className="mt-2 inline-block px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Review
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;