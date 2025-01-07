interface PageContainerProps {
  children: React.ReactNode;
}

export function PageContainer({ children }: PageContainerProps) {
  return (
    <div className="px-4 py-6 md:px-6 max-w-3xl mx-auto">
      {children}
    </div>
  );
} 