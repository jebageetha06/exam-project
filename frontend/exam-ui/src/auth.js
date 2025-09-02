// frontend/src/auth.js

export function isAuthed() {
  return !!localStorage.getItem("token");
}

export function saveToken(token) {
  localStorage.setItem("token", token);
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

// Login function
export async function login(email, password) {
  try { 
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok && data.access_token) {
      saveToken(data.access_token);
      return data.access_token;
    }
    alert(data.detail || "Login failed");
    return null;
  } catch (err) {
    console.error(err);
    return null;
  }
}
