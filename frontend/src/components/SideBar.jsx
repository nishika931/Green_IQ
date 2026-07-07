import { NavLink } from "react-router-dom";
import { X } from "lucide-react";

export default function Sidebar({ open, setOpen }) {
  const menu = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: "🏠",
    },
    {
      name: "Plant Doctor",
      path: "/doctor",
      icon: "🩺",
    },
    {
      name: "Plant Search",
      path: "/search",
      icon: "🔍",
    },
    {
      name: "My Plants",
      path: "/plants",
      icon: "🌱",
    },
    {
      name: "Chat History",
      path: "/history",
      icon: "💬",
    },
  ];

  return (
    <>
      {/* Mobile Overlay */}

      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 bg-black/40 z-40 md:hidden"
        />
      )}

      <aside
        className={`
 fixed
md:sticky
top-0
left-0
h-screen
flex-shrink-0
          w-64
          bg-white
          shadow-xl
          z-50

          flex
          flex-col

          transform
          transition-transform
          duration-300

          ${open ? "translate-x-0" : "-translate-x-full"}

          md:translate-x-0
        `}
      >
        {/* Mobile Header */}

        <div className="flex justify-between items-center p-5 md:hidden">
          <h1 className="font-bold text-green-700 text-xl">Green IQ</h1>

          <button onClick={() => setOpen(false)}>
            <X size={24} />
          </button>
        </div>

        {/* Desktop Logo */}

        <div className="hidden md:block p-6">
          <h1 className="text-2xl font-bold text-green-700">🌿 Green IQ</h1>
        </div>

        {/* Menu */}

        <div className="px-4 space-y-2 flex-1">
          {menu.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `
                flex items-center gap-3
                px-4 py-3
                rounded-xl
                transition

                ${
                  isActive
                    ? "bg-green-600 text-white"
                    : "text-gray-700 hover:bg-green-100"
                }

                `
              }
            >
              <span>{item.icon}</span>

              <span>{item.name}</span>
            </NavLink>
          ))}
        </div>

        {/* Logout */}

        <div className="p-4 border-t">
          <button
            onClick={() => {
              localStorage.removeItem("token");
              localStorage.removeItem("user");

              window.location.href = "/";
            }}
            className="
w-full
py-3
rounded-xl
bg-red-500
text-white
font-semibold
hover:bg-red-600
transition
shadow-md
"
          >
            Logout
          </button>
        </div>
      </aside>
    </>
  );
}
