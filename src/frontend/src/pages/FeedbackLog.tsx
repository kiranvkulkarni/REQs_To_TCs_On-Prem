import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Feedback {
  id: number;
  screenshot_id: number;
  status: string;
  rejection_reason?: string;
  comment?: string;
  created_at: string;
}

const FeedbackLog: React.FC = () => {
  const [feedbacks, setFeedbacks] = useState<Feedback[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFeedbacks = async () => {
      try {
        await axios.get('/api/v1/export'); // Get all for dashboard
        const feedbacksRes = await axios.get('/api/v1/feedback'); // Get feedbacks
        setFeedbacks(feedbacksRes.data.results || []);
        setLoading(false);
      } catch (err: any) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchFeedbacks();
  }, []);

  if (loading) return <div className="text-center p-8">Loading...</div>;
  if (error) return <div className="text-center p-8 text-red-500">Error: {error}</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Feedback Log</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white dark:bg-gray-800 rounded shadow">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">ID</th>
              <th className="py-2 px-4 border-b">Screenshot ID</th>
              <th className="py-2 px-4 border-b">Status</th>
              <th className="py-2 px-4 border-b">Reason</th>
              <th className="py-2 px-4 border-b">Comment</th>
              <th className="py-2 px-4 border-b">Created</th>
            </tr>
          </thead>
          <tbody>
            {feedbacks.map((feedback) => (
              <tr key={feedback.id}>
                <td className="py-2 px-4 border-b">{feedback.id}</td>
                <td className="py-2 px-4 border-b">{feedback.screenshot_id}</td>
                <td className="py-2 px-4 border-b">
                  <span className={`px-2 py-1 rounded text-xs ${
                    feedback.status === 'accepted'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  }`}>
                    {feedback.status}
                  </span>
                </td>
                <td className="py-2 px-4 border-b">{feedback.rejection_reason || "-"}</td>
                <td className="py-2 px-4 border-b">{feedback.comment || "-"}</td>
                <td className="py-2 px-4 border-b">{new Date(feedback.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FeedbackLog;