import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {

  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {

    // Frontend validation
    if (!email.trim()) {
      setError("Please enter your email");
      return;
    }

    if (!password.trim()) {
      setError("Please enter your password");
      return;
    }

    try {

      setLoading(true);
      setError("");

      await login(email, password);

      navigate("/dashboard");

    } catch (err) {

      setError(
        err.response?.data?.detail || "Login Failed"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 via-white to-green-200 flex items-center justify-center p-6">

      <div className="bg-white rounded-[35px] shadow-2xl w-full max-w-5xl overflow-hidden grid lg:grid-cols-2">

        <div className="hidden lg:flex bg-green-600 text-white flex-col justify-center items-center p-10">

          <div className="text-8xl">
            🌿
          </div>

          <h1 className="text-5xl font-bold mt-6">
            Green IQ
          </h1>

          <p className="mt-5 text-center">
            AI Powered Plant Care Assistant
          </p>

        </div>

        <div className="p-10">

          <h2 className="text-4xl font-bold">
            Welcome Back 👋
          </h2>

          <p className="text-gray-500 mt-2">
            Login to continue
          </p>

          <input
            className="w-full border rounded-2xl p-4 mt-8"
            placeholder="Email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setError("");
            }}
          />

          <input
            type="password"
            className="w-full border rounded-2xl p-4 mt-5"
            placeholder="Password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setError("");
            }}
          />

          <button
            onClick={handleLogin}
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-400 disabled:cursor-not-allowed transition text-white rounded-2xl p-4 mt-8"
          >

            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Logging in...
              </span>
            ) : (
              "Login"
            )}

          </button>

          {error && (
            <p className="mt-4 text-center text-red-500 font-medium">
              {error}
            </p>
          )}

          <p className="mt-6 text-center">

            Don't have an account?

            <Link
              to="/register"
              className="ml-2 text-green-700 font-semibold"
            >
              Register
            </Link>

          </p>

        </div>

      </div>

    </div>
  );
}

