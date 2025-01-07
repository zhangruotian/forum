import { PageContainer } from '../components/PageContainer';

export function HomePage() {
  return (
    <PageContainer>
      <div className="text-center">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Welcome to Forum</h1>
        <p className="mt-4 text-base sm:text-lg text-gray-600">
          Start exploring articles or create your own.
        </p>
      </div>
    </PageContainer>
  );
} 