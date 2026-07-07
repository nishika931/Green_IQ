import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Doctor from "./pages/Doctor";
import Search from "./pages/Search";
import MyPlants from "./pages/MyPlants";
import History from "./pages/History";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");

  return token ? children : <Navigate to="/" />;
}

export default function App() {
  return (
    <Routes>

      {/* Auth */}
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Dashboard */}
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />

      {/* Doctor */}
      <Route
        path="/doctor"
        element={
          <PrivateRoute>
            <Doctor />
          </PrivateRoute>
        }
      />

      {/* Search */}
      <Route
        path="/search"
        element={
          <PrivateRoute>
            <Search />
          </PrivateRoute>
        }
      />

      {/* Plants */}
      <Route
        path="/plants"
        element={
          <PrivateRoute>
            <MyPlants />
          </PrivateRoute>
        }
      />

      {/* History */}
      <Route
        path="/history"
        element={
          <PrivateRoute>
            <History />
          </PrivateRoute>
        }
      />

    </Routes>
  );
}