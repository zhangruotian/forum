import sys
from pathlib import Path

# Add the project root directory to Python path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal
from app.models.article import Article
from app.models.user import User


def fix_counts():
    db = SessionLocal()
    try:
        print("Starting count fix...")

        # Fix article counts
        users = db.query(User).all()
        print(f"Found {len(users)} users")

        for user in users:
            print(f"\nProcessing user {user.id}:")

            article_count = (
                db.query(Article).filter(Article.author_id == user.id).count()
            )
            print(f"- Articles: {article_count}")
            user.article_count = article_count

            comment_count = sum(len(article.comments) for article in user.articles)
            print(f"- Comments: {comment_count}")
            user.comment_count = comment_count

        # Fix comment counts for articles
        articles = db.query(Article).all()
        print(f"\nFound {len(articles)} articles")

        for article in articles:
            old_count = article.comment_count
            new_count = len(article.comments)
            print(f"Article {article.id}: {old_count} -> {new_count} comments")
            article.comment_count = new_count

        db.commit()
        print("\nCounts fixed successfully!")

    except Exception as e:
        print(f"\nError fixing counts: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_counts()
