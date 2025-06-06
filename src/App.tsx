import React, { useState } from 'react';
import SignUp from './components/SignUp';
import Login from './components/Login';
import ChatBot from './components/ChatBot'; // Import ChatBot component

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false); // State to manage login status

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Show either SignUp or Login based on state */}
      {isLoggedIn ? (
        <>
          <ChatBot /> {/* Show ChatBot when logged in */}
          <div className="fixed bottom-4 right-4">
            <button
              onClick={() => setIsLoggedIn(false)} // Log out the user
              className="bg-white px-6 py-2 rounded-lg shadow-md text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Log Out
            </button>
          </div>
        </>
      ) : showLogin ? (
        <Login onLoginSuccess={() => setIsLoggedIn(true)} /> // If login is successful, show ChatBot
      ) : (
        <SignUp />
      )}
      
      <div className="fixed bottom-4 right-4">
        <button
          onClick={() => setShowLogin(!showLogin)}
          className="bg-white px-6 py-2 rounded-lg shadow-md text-gray-700 hover:bg-gray-50 transition-colors"
        >
          {showLogin ? 'Need an account? Sign Up' : 'Already have an account? Log In'}
        </button>
      </div>
    </div>
  );
}

export default App;
