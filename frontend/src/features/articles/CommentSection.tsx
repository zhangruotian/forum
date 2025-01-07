import { Link } from 'react-router-dom';

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

interface CommentSectionProps {
  comments: Comment[];
}

export function CommentSection({ comments }: CommentSectionProps) {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">Comments ({comments.length})</h2>
      <div className="space-y-4">
        {comments.map((comment) => (
          <div key={comment.id} className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Link 
                to={`/users/${comment.author.id}`}
                className="text-blue-600 hover:text-blue-800 hover:underline cursor-pointer"
              >
                {comment.author.full_name}
              </Link>
              <span className="text-gray-500">•</span>
              <time className="text-gray-500">
                {new Date(comment.created_at).toLocaleDateString()}
              </time>
            </div>
            <p className="text-gray-700 whitespace-pre-wrap mt-2">{comment.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
} 