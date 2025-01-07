import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { articles, Article } from '../../lib/api';

export function ArticleList() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [articleList, setArticleList] = useState<Article[]>([]);

  useEffect(() => {
    const fetchArticles = async () => {
      console.log('Fetching articles...'); // Debug log
      try {
        const data = await articles.list();
        console.log('Articles response:', data); // Debug log
        setArticleList(data.items || []);
      } catch (err: any) {
        console.error('Error fetching articles:', err); // Debug log
        console.error('Error details:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
        });
        setError(err.response?.data?.detail || 'Failed to load articles');
      } finally {
        setIsLoading(false);
      }
    };

    fetchArticles();
  }, []);

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 text-red-600">
        <p>{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 text-primary-600 hover:text-primary-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Articles</h1>
        <Link 
          to="/articles/new" 
          className="btn btn-primary w-full sm:w-auto"
        >
          Write Article
        </Link>
      </div>

      {articleList.length === 0 ? (
        <div className="text-center py-8 bg-white rounded-lg shadow-sm">
          <p className="text-gray-500">No articles yet. Be the first to write one!</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {articleList.map((article) => (
            <Link
              key={article.id}
              to={`/articles/${article.id}`}
              className="block p-4 sm:p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2 line-clamp-2">
                {article.title}
              </h2>
              {article.summary && (
                <p className="text-sm sm:text-base text-gray-600 mb-4 line-clamp-2">
                  {article.summary}
                </p>
              )}
              <div className="flex items-center justify-between text-sm text-gray-500">
                <span className="flex items-center">
                  <span className="mr-1">💬</span>
                  {article.comment_count}
                </span>
                <span className="text-gray-600">
                  by {article.author.full_name}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
} 