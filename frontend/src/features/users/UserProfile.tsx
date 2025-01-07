import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { User, Article, Comment, api } from '../../lib/api';
import { useAuth } from '../../hooks/useAuth';

export function UserProfile() {
  const { id } = useParams();
  const { user: currentUser } = useAuth();
  const [user, setUser] = useState<User | null>(null);
  const [articles, setArticles] = useState<Article[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUserProfile = async () => {
    try {
      const response = await api.get(`/users/${id}`);
      console.log('User profile response:', response.data); // Debug log
      setUser(response.data);
      setArticles(response.data.recent_articles);
      setComments(response.data.recent_comments);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching profile:', err);
      setError(err.response?.data?.detail || 'Failed to load profile');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    fetchUserProfile();
  }, [id]);

  const handleAvatarUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files?.length) return;
    
    const file = event.target.files[0];
    console.log('Uploading file:', file);  // Debug log
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Making request to:', `/users/${user?.id}/avatar`);  // Debug log
      const response = await api.post(`/users/${user?.id}/avatar`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Upload response:', response);  // Debug log
      // Refresh user data
      fetchUserProfile();
    } catch (error: any) {
      console.error('Failed to upload avatar:', error);
      setError(error.response?.data?.detail || 'Failed to upload avatar');
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading profile...</div>;
  }

  if (error || !user) {
    return <div className="text-red-600">{error || 'User not found'}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
              {user.avatar_url ? (
                <img 
                  src={user.avatar_url} 
                  alt={user.full_name} 
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    console.error('Failed to load image:', user.avatar_url); // Debug log
                    e.currentTarget.style.display = 'none';
                    e.currentTarget.parentElement?.classList.add('fallback');
                  }}
                />
              ) : (
                <span className="text-2xl">{user.full_name[0].toUpperCase()}</span>
              )}
            </div>
            
            {/* Only show upload button for current user */}
            {currentUser?.id === user.id && (
              <label className="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-md cursor-pointer hover:bg-gray-50">
                <input
                  type="file"
                  className="hidden"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                />
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  className="w-4 h-4 text-gray-600"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" 
                  />
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" 
                  />
                </svg>
              </label>
            )}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{user.full_name}</h1>
            <p className="text-gray-500">{user.email}</p>
          </div>
        </div>
        <div className="mt-6 grid grid-cols-2 gap-4 text-center">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-2xl font-bold text-primary-600">{user.article_count}</div>
            <div className="text-sm text-gray-500">Articles</div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-2xl font-bold text-primary-600">{user.comment_count}</div>
            <div className="text-sm text-gray-500">Comments</div>
          </div>
        </div>
        <div className="mt-4 text-sm text-gray-500">
          Member since {new Date(user.created_at).toLocaleDateString()}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid gap-8 md:grid-cols-2">
        {/* Recent Articles */}
        <div>
          <h2 className="text-xl font-bold mb-4">Recent Articles</h2>
          <div className="space-y-4">
            {articles.length === 0 ? (
              <p className="text-gray-500">No articles yet</p>
            ) : (
              articles.map(article => (
                <Link
                  key={article.id}
                  to={`/articles/${article.id}`}
                  className="block bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow"
                >
                  <h3 className="font-semibold text-gray-900 mb-2">{article.title}</h3>
                  {article.summary && (
                    <p className="text-gray-600 text-sm mb-2 line-clamp-2">{article.summary}</p>
                  )}
                  <div className="text-sm text-gray-500">
                    {new Date(article.created_at).toLocaleDateString()}
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>

        {/* Recent Comments */}
        <div>
          <h2 className="text-xl font-bold mb-4">Recent Comments</h2>
          <div className="space-y-4">
            {comments.length === 0 ? (
              <p className="text-gray-500">No comments yet</p>
            ) : (
              comments.map(comment => (
                <Link
                  key={comment.id}
                  to={`/articles/${comment.article_id}`}
                  className="block bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow"
                >
                  <p className="text-gray-700 mb-2 line-clamp-3">{comment.content}</p>
                  <div className="text-sm text-gray-500">
                    {new Date(comment.created_at).toLocaleDateString()}
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 