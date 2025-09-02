import { useEffect, useState } from "react";

export default function Timer({ seconds=1800, onExpire }){
  const [left, setLeft] = useState(seconds);
  useEffect(() => {
    const id = setInterval(() => {
      setLeft(l => {
        if (l <= 1) { clearInterval(id); onExpire?.(); return 0; }
        return l - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [onExpire]);

  const mm = String(Math.floor(left/60)).padStart(2,'0');
  const ss = String(left%60).padStart(2,'0');
  return <div>Time Left: {mm}:{ss}</div>;
}
