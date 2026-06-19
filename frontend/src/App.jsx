import { useEffect, useState } from "react";
import { getMe, getToken } from "./api/client";
import AuthModal from "./components/AuthModal";
import LandingPage from "./components/LandingPage";
import Chat from "./components/Chat";
import "./App.css";

export default function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [email, setEmail] = useState("");
  const [checking, setChecking] = useState(true);
  const [authModal, setAuthModal] = useState(null);

  useEffect(() => {
    if (!getToken()) {
      setChecking(false);
      return;
    }
    getMe()
      .then((user) => {
        setEmail(user.email);
        setAuthenticated(true);
      })
      .catch(() => setAuthenticated(false))
      .finally(() => setChecking(false));
  }, []);

  function handleAuthSuccess() {
    getMe().then((user) => {
      setEmail(user.email);
      setAuthenticated(true);
      setAuthModal(null);
    });
  }

  if (checking) {
    return (
      <div className="app-loading">
        <div className="spinner" aria-hidden="true" />
        <p>Loading…</p>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <>
        <LandingPage
          onOpenLogin={() => setAuthModal("login")}
          onOpenRegister={() => setAuthModal("register")}
        />
        {authModal && (
          <AuthModal
            mode={authModal}
            onClose={() => setAuthModal(null)}
            onSuccess={handleAuthSuccess}
            onSwitchMode={setAuthModal}
          />
        )}
      </>
    );
  }

  return (
    <Chat
      email={email}
      onLogout={() => {
        setAuthenticated(false);
        setEmail("");
      }}
    />
  );
}
