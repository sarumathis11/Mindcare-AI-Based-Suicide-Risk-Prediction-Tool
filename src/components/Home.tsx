import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold">Home Page</h1>
      <button
        onClick={() => navigate('/login')}
        className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg shadow-md hover:bg-blue-700"
      >
        Go to Login
      </button>
    </div>
  );
};

export default Home;
