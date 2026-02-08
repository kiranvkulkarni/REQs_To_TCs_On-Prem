import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Screenshot {
  id: number;
  filename: string;
  feature_name: string;
  gestures: any[];
  conditions: string[];
  errors: string[];
  languages: string[];
  gherkin: string;
  status: string;
  rejection_reason?: string;
  comment?: string;
}

const Review: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [screenshot, setScreenshot] = useState<Screenshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedReason, setSelectedReason] = useState<string>("");
  const [comment, setComment] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchScreenshot = async () => {
      try {
        await axios.get(`/api/v1/ingest`); // Ensure ingest is done
        await axios.get(`/api/v1/generate`); // Ensure generate is done
        const screenshotRes = await axios.get(`/api/v1/export`); // Get all for dashboard
        const found = screenshotRes.data.results.find((s: any) => s.id === parseInt(id!));
        if (found) {
          setScreenshot(found);
        } else {
          setError("Screenshot not found");
        }
        setLoading(false);
      } catch (err: any) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchScreenshot();
  }, [id]);

  const handleAccept = async () => {
    try {
      setIsSubmitting(true);
      await axios.post('/api/v1/feedback', {
        screenshot_id: screenshot?.id,
        status: "accepted"
      });
      alert("Test case accepted!");
      navigate('/');
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReject = async () => {
    if (!selectedReason) {
      alert("Please select a rejection reason");
      return;
    }
    try {
      setIsSubmitting(true);
      await axios.post('/api/v1/feedback', {
        screenshot_id: screenshot?.id,
        status: "rejected",
        rejection_reason: selectedReason,
        comment: comment
      });
      alert("Test case rejected!");
      navigate('/');
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) return <div className="text-center p-8">Loading...</div>;
  if (error) return <div className="text-center p-8 text-red-500">Error: {error}</div>;
  if (!screenshot) return <div className="text-center p-8">Screenshot not found</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Review: {screenshot.feature_name}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded shadow-md bg-white dark:bg-gray-800">
          <h2 className="font-bold">Screenshot</h2>
          <img
            src={`/data/input_screenshots/${screenshot.filename}`}
            alt={screenshot.filename}
            className="mt-2 max-w-full h-auto rounded"
          />
          <p className="mt-2 text-sm text-gray-500">File: {screenshot.filename}</p>
          <p className="text-sm text-gray-500">Status: {screenshot.status}</p>
        </div>
        <div className="p-4 rounded shadow-md bg-white dark:bg-gray-800">
          <h2 className="font-bold">Generated Gherkin</h2>
          <pre className="mt-2 p-2 bg-gray-100 dark:bg-gray-700 rounded overflow-auto text-sm">
            {screenshot.gherkin || "No Gherkin generated"}
          </pre>
          <div className="mt-4">
            <button
              onClick={handleAccept}
              disabled={isSubmitting}
              className="mr-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
            >
              {isSubmitting ? "Accepting..." : "Accept"}
            </button>
            <button
              onClick={handleReject}
              disabled={isSubmitting}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
            >
              {isSubmitting ? "Rejecting..." : "Reject"}
            </button>
          </div>
        </div>
      </div>
      {screenshot.status === "rejected" && (
        <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 rounded">
          <h3 className="font-bold">Rejection Details</h3>
          <p><strong>Reason:</strong> {screenshot.rejection_reason}</p>
          <p><strong>Comment:</strong> {screenshot.comment}</p>
        </div>
      )}
      {screenshot.status !== "rejected" && (
        <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-700 rounded">
          <h3 className="font-bold">Reject Test Case</h3>
          <select
            value={selectedReason}
            onChange={(e) => setSelectedReason(e.target.value)}
            className="mt-2 p-2 border rounded w-full"
          >
            <option value="">Select reason...</option>
            {[
              "Wrong gesture interpretation",
              "Missing error state",
              "Over-creation (not in screenshot)",
              "Incorrect language translation",
              "Invalid condition logic",
              "UI element misidentified"
            ].map((reason) => (
              <option key={reason} value={reason}>{reason}</option>
            ))}
          </select>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Add optional comment..."
            className="mt-2 p-2 border rounded w-full"
            rows={3}
          />
        </div>
      )}
    </div>
  );
};

export default Review;