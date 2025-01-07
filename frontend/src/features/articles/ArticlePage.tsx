import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../../lib/api';
import { CommentSection } from './CommentSection';

interface Author {
  id: number;
  full_name: string;
  email: string;
}

interface Comment {
  id: number;
  content: string;
  created_at: string;
  updated_at: string;
  author: Author;
  article_id: number;
}

interface Article {
  id: number;
  title: string;
  content: string;
  created_at: string;
  author: Author;
  comments: Comment[];
}

export function ArticlePage() {
  const { id } = useParams();
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    const fetchArticle = async () => {
      try {
        const response = await api.get(`/articles/${id}`, {
          signal: controller.signal
        });
        setArticle(response.data);
      } catch (error) {
        console.error('Error fetching article:', error);
        setError('Failed to load article');
      }
    };

    fetchArticle();

    return () => {
      controller.abort();
    };
  }, [id]);

  if (error) return <div className="text-red-500">{error}</div>;
  if (!article) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <article className="prose lg:prose-xl">
        <h1>{article.title}</h1>
        <div className="flex items-center gap-2 text-gray-600">
          <Link 
            to={`/users/${article.author.id}`}
            className="text-blue-600 hover:text-blue-800 hover:underline"
          >
            {article.author.full_name}
          </Link>
          <span>•</span>
          <time>{new Date(article.created_at).toLocaleDateString()}</time>
        </div>
        <div className="mt-4">{article.content}</div>
      </article>

      <CommentSection comments={article.comments} />
    </div>
  );
} 