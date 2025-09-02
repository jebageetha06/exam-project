import { useState } from "react";
import Timer from "../components/Timer";
import { useNavigate } from "react-router-dom";

// 10 Java questions
const questions = [
  {
    id: 1,
    question: "What is the default value of int in Java?",
    options: ["0", "null", "1", "-1"],
    answer: "0"
  },
  {
    id: 2,
    question: "Which keyword is used to inherit a class in Java?",
    options: ["implements", "inherits", "extends", "super"],
    answer: "extends"
  },
  {
    id: 3,
    question: "What does JVM stand for?",
    options: ["Java Very Much", "Java Virtual Machine", "Java Variable Method", "Java Version Manager"],
    answer: "Java Virtual Machine"
  },
  {
    id: 4,
    question: "Which of these is not a primitive type in Java?",
    options: ["int", "float", "String", "boolean"],
    answer: "String"
  },
  {
    id: 5,
    question: "Which method is the entry point of a Java program?",
    options: ["start()", "main()", "init()", "run()"],
    answer: "main()"
  },
  {
    id: 6,
    question: "What is the size of boolean in Java?",
    options: ["1 byte", "Depends on JVM", "4 bytes", "2 bytes"],
    answer: "Depends on JVM"
  },
  {
    id: 7,
    question: "Which exception is thrown when dividing by zero?",
    options: ["IOException", "ArithmeticException", "NullPointerException", "ClassNotFoundException"],
    answer: "ArithmeticException"
  },
  {
    id: 8,
    question: "Which of these is a checked exception?",
    options: ["IOException", "ArithmeticException", "NullPointerException", "ArrayIndexOutOfBoundsException"],
    answer: "IOException"
  },
  {
    id: 9,
    question: "Which of these is not a Java access modifier?",
    options: ["private", "protected", "package", "public"],
    answer: "package"
  },
  {
    id: 10,
    question: "What is the parent class of all classes in Java?",
    options: ["Object", "Class", "Parent", "Root"],
    answer: "Object"
  }
];

export default function Exam() {
  const [answers, setAnswers] = useState({});
  const nav = useNavigate();

  const handleOptionChange = (qId, option) => {
    setAnswers(prev => ({ ...prev, [qId]: option }));
  };

  const handleSubmit = () => {
    // Save answers to localStorage for Result page
    localStorage.setItem("answers", JSON.stringify(answers));
    nav("/result");
  };

  return (
    <div>
      <h2>Java Exam</h2>
      <Timer seconds={1800} onExpire={handleSubmit} /> {/* 30 min timer */}

      {questions.map(q => (
        <div key={q.id} style={{ marginBottom: 20 }}>
          <p>{q.id}. {q.question}</p>
          {q.options.map(opt => (
            <label key={opt} style={{ display: "block" }}>
              <input
                type="radio"
                name={`q${q.id}`}
                value={opt}
                checked={answers[q.id] === opt}
                onChange={() => handleOptionChange(q.id, opt)}
              />{" "}
              {opt}
            </label>
          ))}
        </div>
      ))}

      <button onClick={handleSubmit}>Submit Exam</button>
    </div>
  );
}

