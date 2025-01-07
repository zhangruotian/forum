import { useState, useEffect } from 'react';
import { comments, Comment, CreateCommentData } from '../../lib/api';
import { Link } from 'react-router-dom';

interface CommentSectionProps {
  articleId: number;
  onCommentChange?: () => void;
}

export function CommentSection({ articleId, onCommentChange }: CommentSectionProps) {
  const [commentList, setCommentList] = useState<Comment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newComment, setNewComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchComments = async () => {
    console.log('Fetching comments...'); // Debug log
    try {
      const data = await comments.list(articleId);
      console.log('Fetched comments:', data); // Debug log
      setCommentList(Array.isArray(data) ? data : data.items || []);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching comments:', err); // Debug log
      setError(err.response?.data?.detail || 'Failed to load comments');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    fetchComments();
  }, [articleId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setIsSubmitting(true);
    setError(null); // Clear any previous errors
    console.log('Submitting comment...'); // Debug log

    try {
      const response = await comments.create(articleId, { content: newComment.trim() });
      console.log('Comment created:', response); // Debug log
      setNewComment('');
      await fetchComments();
      onCommentChange?.();
    } catch (err: any) {
      console.error('Error creating comment:', err); // Debug log
      setError(err.response?.data?.detail || 'Failed to post comment');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <div className="animate-pulse">Loading comments...</div>;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl sm:text-2xl font-bold text-gray-900">
        Comments ({commentList.length})
      </h2>

      {/* Comment Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="comment" className="sr-only">
            Add a comment
          </label>
          <textarea
            id="comment"
            rows={3}
            className={`input w-full ${isSubmitting ? 'opacity-50' : ''}`}
            placeholder="Add a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            disabled={isSubmitting}
          />
        </div>
        <div className="flex justify-between items-center">
          {error && (
            <p className="text-sm text-red-600">
              {error}
            </p>
          )}
          <button
            type="submit"
            className="btn btn-primary ml-auto"
            disabled={isSubmitting || !newComment.trim()}
          >
            {isSubmitting ? (
              <>
                <span className="animate-spin mr-2">⏳</span>
                Posting...
              </>
            ) : (
              'Post Comment'
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="p-3 text-sm text-red-700 bg-red-50 rounded-lg">
          {error}
        </div>
      )}

      {/* Comments List */}
      <div className="space-y-4">
        {commentList.length === 0 ? (
          <p className="text-gray-500 text-center py-4">
            No comments yet. Be the first to comment!
          </p>
        ) : (
          commentList.map((comment) => (
            <div
              key={comment.id}
              className="p-4 bg-white rounded-lg shadow-sm space-y-2"
            >
              <div className="flex justify-between items-start">
                <div className="flex flex-col">
                  <Link
                    to={`/users/${comment.author.id}`}
                    className="text-gray-600 hover:text-blue-600"
                  >
                    By {comment.author.full_name}
                  </Link>
                  <span className="text-sm text-gray-500">
                    {new Date(comment.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <div className="text-gray-700 whitespace-pre-wrap">
                {comment.content}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
} 