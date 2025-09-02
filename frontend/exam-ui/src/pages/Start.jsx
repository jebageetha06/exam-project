import { Link } from "react-router-dom";

export default function Start() {
  return (
    <div>
      <h2>Welcome to the Exam</h2>
      <p>Click below to start your exam.</p>
      <Link to="/exam">
        <button>Start Exam</button>
      </Link>
    </div>
  );
}
