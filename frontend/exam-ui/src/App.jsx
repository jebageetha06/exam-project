import { Routes, Route, Navigate, Link } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Start from "./pages/Start";
import Exam from "./pages/Exam";
import Result from "./pages/Result";
import ProtectedRoute from "./components/ProtectedRoute";
import { logout, isAuthed } from "./auth";

export default function App() {
  return (
    <div style={{ maxWidth: 800, margin: "20px auto", padding: 16 }}>
      <header style={{ display: "flex", justifyContent: "space-between" }}>
        <Link to="/">Exam App</Link>
        {isAuthed() && <button onClick={logout}>Logout</button>}
      </header>

      <Routes>
        <Route path="/" element={<Navigate to="/register" />} /> {/* Default goes to register first */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/start"
          element={
            <ProtectedRoute>
              <Start />
            </ProtectedRoute>
          }
        />
        <Route
          path="/exam"
          element={
            <ProtectedRoute>
              <Exam />
            </ProtectedRoute>
          }
        />
        <Route
          path="/result"
          element={
            <ProtectedRoute>
              <Result />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
}


