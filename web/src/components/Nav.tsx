"use client";

import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Overview" },
  { href: "/dataset", label: "Dataset" },
  { href: "/documentation", label: "Documentation" },
  { href: "/results", label: "Results" },
  { href: "/whitepaper", label: "White Paper" },
];

export function Nav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <a
          href="/"
          className="text-xl font-bold tracking-tight text-amber-600 hover:text-amber-700"
        >
          PSAE
        </a>
        <ul className="flex gap-6">
          {navItems.map(({ href, label }) => (
            <li key={href}>
              <a
                href={href}
                className={`text-sm font-medium transition-colors ${
                  pathname === href
                    ? "text-amber-600"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                {label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
