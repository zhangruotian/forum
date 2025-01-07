import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginForm } from './features/auth/LoginForm';
import { RegisterForm } from './features/auth/RegisterForm';
import { AuthLayout } from './layouts/AuthLayout';
import { ProtectedLayout } from './layouts/ProtectedLayout';
import { HomePage } from './pages/HomePage';
import { ArticleList } from './features/articles/ArticleList';
import { ArticleCreate } from './features/articles/ArticleCreate';
import { ArticleDetail } from './features/articles/ArticleDetail';
import { UserProfile } from './features/users/UserProfile';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
        </Route>

        {/* Protected routes */}
        <Route element={<ProtectedLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/articles" element={<ArticleList />} />
          <Route path="/articles/new" element={<ArticleCreate />} />
          <Route path="/articles/:id" element={<ArticleDetail />} />
          <Route path="/users/:id" element={<UserProfile />} />
        </Route>

        {/* Redirect any unknown routes to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
