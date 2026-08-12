import { Navigate, Route, Routes } from "react-router-dom";
import SiteLayout from "./components/SiteLayout.jsx";
import Demo from "./pages/Demo.jsx";
import Documentation from "./pages/Documentation.jsx";
import Home from "./pages/Home.jsx";
import HowItWorks from "./pages/HowItWorks.jsx";

export default function App() {
  return (
    <SiteLayout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/demo" element={<Demo />} />
        <Route path="/documentation" element={<Documentation />} />
        <Route path="*" element={<Navigate replace to="/" />} />
      </Routes>
    </SiteLayout>
  );
}
