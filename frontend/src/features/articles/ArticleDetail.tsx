import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { articles, Article } from '../../lib/api';
import { CommentSection } from '../comments/CommentSection';

export function ArticleDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState<Article | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchArticle = async () => {
    if (!id) return;
    
    try {
      const data = await articles.get(parseInt(id));
      setArticle(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load article');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    fetchArticle();
  }, [id]);

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="text-center py-8 text-red-600">
        {error || 'Article not found'}
      </div>
    );
  }

  return (
    <div className="px-4 py-6 md:px-6 max-w-3xl mx-auto">
      {/* Article Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
          {article.title}
        </h1>
        <div className="flex items-center text-sm text-gray-500 space-x-4">
          <Link to={`/users/${article.author_id}`} className="hover:text-primary-600">
            By {article.author.full_name}
          </Link>
          <span>•</span>
          <span>{new Date(article.created_at).toLocaleDateString()}</span>
          {article.status === 'draft' && (
            <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
              Draft
            </span>
          )}
        </div>

        {/* Tags */}
        {article.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 my-4">
            {article.tags.map(tag => (
              <span
                key={tag}
                className="px-2 py-1 text-sm bg-blue-100 text-blue-800 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Summary */}
        {article.summary && (
          <div className="my-6 text-base sm:text-lg text-gray-600 border-l-4 border-gray-200 pl-4">
            {article.summary}
          </div>
        )}
      </div>

      {/* Article Content */}
      <div 
        className="prose max-w-none mb-8 text-base sm:text-lg"
        dangerouslySetInnerHTML={{ __html: article.content }}
      />

      {/* Article Footer */}
      <div className="border-t border-gray-200 pt-4 mt-8">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
          <div className="flex items-center space-x-6 text-sm text-gray-500">
            <span className="flex items-center">
              <span className="mr-2">👁</span>
              {article.comment_count} comments
            </span>
          </div>
          <button
            onClick={() => navigate('/articles')}
            className="text-primary-600 hover:text-primary-700 text-sm"
          >
            Back to Articles
          </button>
        </div>
      </div>

      {/* Comments Section */}
      <div className="mt-8">
        <CommentSection 
          articleId={parseInt(id!)} 
          onCommentChange={fetchArticle}
        />
      </div>
    </div>
  );
} 