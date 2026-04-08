import { useState } from "react";
import { Link, NavLink } from "react-router-dom";

const navItems = [
  { label: "Home", to: "/" },
  { label: "Analyse", to: "/upload" },
  { label: "History", to: "/upload" },
];

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const linkClasses = ({ isActive }) =>
    `rounded-full px-3 py-2 text-sm font-medium transition ${
      isActive
        ? "bg-emerald-600 text-white"
        : "text-emerald-800 hover:bg-emerald-100 hover:text-emerald-900"
    }`;

  return (
    <header className="sticky top-0 z-40 border-b border-emerald-100 bg-white/85 backdrop-blur">
      <nav className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-full bg-emerald-600 text-center text-xl leading-9 text-white">
            P
          </div>
          <span className="text-lg font-bold tracking-wide text-emerald-900">PlantDoc</span>
        </Link>

        <button
          type="button"
          className="rounded-lg border border-emerald-200 p-2 text-emerald-800 md:hidden"
          onClick={() => setIsOpen((prev) => !prev)}
          aria-label="Toggle navigation menu"
        >
          <span className="block h-0.5 w-5 bg-current" />
          <span className="mt-1 block h-0.5 w-5 bg-current" />
          <span className="mt-1 block h-0.5 w-5 bg-current" />
        </button>

        <div className="hidden items-center gap-2 md:flex">
          {navItems.map((item) => (
            <NavLink key={item.label} to={item.to} className={linkClasses}>
              {item.label}
            </NavLink>
          ))}
        </div>
      </nav>

      {isOpen && (
        <div className="border-t border-emerald-100 px-4 pb-3 md:hidden">
          <div className="flex flex-col gap-2 pt-3">
            {navItems.map((item) => (
              <NavLink
                key={item.label}
                to={item.to}
                className={linkClasses}
                onClick={() => setIsOpen(false)}
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      )}
    </header>
  );
}

export default Navbar;
