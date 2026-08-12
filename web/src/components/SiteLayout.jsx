import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }) => (isActive ? "nav-link active" : "nav-link");

export default function SiteLayout({ children }) {
  return (
    <div className="site-shell">
      <header className="site-header">
        <NavLink className="wordmark" to="/" aria-label="ExpertTrace home">
          <span className="wordmark-mark" aria-hidden="true">ET</span>
          <span>ExpertTrace</span>
        </NavLink>
        <nav className="main-nav" aria-label="Primary navigation">
          <NavLink className={linkClass} to="/how-it-works">How it works</NavLink>
          <NavLink className={linkClass} to="/demo">Demo</NavLink>
          <NavLink className={linkClass} to="/documentation">Python SDK</NavLink>
          <a className="nav-link nav-external" href="https://github.com/elythera-lab/experttrace">GitHub ↗</a>
        </nav>
      </header>
      {children}
      <footer className="site-footer">
        <div>
          <div className="wordmark footer-wordmark"><span className="wordmark-mark">ET</span><span>ExpertTrace</span></div>
          <p>Open-source infrastructure for knowledge that can be reviewed, reused, and improved.</p>
        </div>
        <div className="footer-links">
          <a href="https://github.com/elythera-lab/experttrace">Source code</a>
          <a href="https://pypi.org/project/elythera-experttrace/">PyPI package</a>
          <a href="https://github.com/elythera-lab/experttrace/issues">Issues</a>
          <a href="https://github.com/elythera-lab/experttrace/blob/main/CONTRIBUTING.md">Contribute</a>
          <a href="https://github.com/elythera-lab/experttrace/blob/main/LICENSE">Apache 2.0</a>
        </div>
      </footer>
    </div>
  );
}
