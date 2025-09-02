import { Link } from "react-router-dom";

const questions = [
  { id: 1, answer: "0" },
  { id: 2, answer: "extends" },
  { id: 3, answer: "Java Virtual Machine" },
  { id: 4, answer: "String" },
  { id: 5, answer: "main()" },
  { id: 6, answer: "Depends on JVM" },
  { id: 7, answer: "ArithmeticException" },
  { id: 8, answer: "IOException" },
  { id: 9, answer: "package" },
  { id: 10, answer: "Object" }
];

export default function Result() {
  const answers = JSON.parse(localStorage.getItem("answers") || "{}");

  // Calculate score
  const score = questions.reduce((acc, q) => {
    if (answers[q.id] === q.answer) return acc + 1;
    return acc;
  }, 0);

  return (
    <div>
      <h2>Exam Result</h2>
      <p>Your score: {score} / {questions.length}</p>
      <Link to="/start">
        <button>Back to Start</button>
      </Link>
    </div>
  );
}
