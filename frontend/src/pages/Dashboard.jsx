import { useState } from "react";
import Sidebar from "../components/SideBar";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {

  const navigate = useNavigate();

  const [sidebarOpen,setSidebarOpen] = useState(false);

  const cards = [
    {
      title: "Plant Doctor",
      icon: "🩺",
      desc: "Diagnose diseases and get AI treatment suggestions.",
      path: "/doctor",
      color: "from-green-500 to-emerald-600"
    },
    {
      title: "Plant Search",
      icon: "🔍",
      desc: "Search thousands of plants with AI care guides.",
      path: "/search",
      color: "from-lime-500 to-green-600"
    },
    {
      title: "My Plants",
      icon: "🪴",
      desc: "Manage and monitor your personal garden.",
      path: "/plants",
      color: "from-teal-500 to-green-600"
    },
    {
      title: "Chat History",
      icon: "💬",
      desc: "View all previous AI conversations.",
      path: "/history",
      color: "from-emerald-500 to-green-700"
    }
  ];

  return (

    <div className="flex min-h-screen bg-[#F4FBF6]">

      <Sidebar 
open={sidebarOpen}
setOpen={setSidebarOpen}
/>

      <div className="flex-1 md:ml-4">

        <Navbar 
setSidebarOpen={setSidebarOpen}
showGreeting={true}
/>
        <div className="p-4 md:p-8 ">

          {/* Hero */}

          <div className="bg-gradient-to-r from-green-700 via-green-600 to-emerald-500 rounded-3xl p-6 md:p-10 text-white shadow-xl">

            <h1 className="text-2xl sm:text-3xl md:text-5xl font-bold">

              🌿 Welcome to Green IQ

            </h1>

            <p className="mt-4 text-base md:text-xl text-green-100">

              Your AI-powered Plant Care Assistant

            </p>

            <p className="mt-2 text-green-50 max-w-3xl">

              Diagnose diseases, search plants, manage your garden,
              and receive intelligent care recommendations using AI.

            </p>

          </div>

          {/* Stats */}

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8">

            <div className="bg-white rounded-2xl shadow-md p-5 text-center">

              <div className="text-4xl">🪴</div>

              <h2 className="text-3xl font-bold text-green-700 mt-2">

                1000+

              </h2>

              <p className="text-gray-500">

                Plants Database

              </p>

            </div>

            <div className="bg-white rounded-2xl shadow-md p-5 text-center">

              <div className="text-4xl">🤖</div>

              <h2 className="text-3xl font-bold text-green-700 mt-2">

                AI

              </h2>

              <p className="text-gray-500">

                Smart Doctor

              </p>

            </div>

            <div className="bg-white rounded-2xl shadow-md p-5 text-center">

              <div className="text-4xl">🌱</div>

              <h2 className="text-3xl font-bold text-green-700 mt-2">

                Care

              </h2>

              <p className="text-gray-500">

                Personalized Advice

              </p>

            </div>

            <div className="bg-white rounded-2xl shadow-md p-5 text-center">

              <div className="text-4xl">💚</div>

              <h2 className="text-3xl font-bold text-green-700 mt-2">

                Healthy

              </h2>

              <p className="text-gray-500">

                Plant Companion

              </p>

            </div>

          </div>

          {/* Features */}

          <h2 className="text-2xl md:text-3xl font-bold text-green-700 mt-10 mb-6">

            Explore Features

          </h2>

          <div className="grid sm:grid-cols-2 xl:grid-cols-2 gap-6">

            {cards.map((card) => (

              <div
                key={card.title}
                onClick={() => navigate(card.path)}
                className="group cursor-pointer bg-white rounded-3xl shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden"
              >

                <div className={`bg-gradient-to-r ${card.color} p-6`}>

                  <div className="text-5xl">

                    {card.icon}

                  </div>

                </div>

                <div className="p-6">

                  <h3 className="text-2xl font-bold text-gray-800 group-hover:text-green-700">

                    {card.title}

                  </h3>

                  <p className="text-gray-500 mt-3">

                    {card.desc}

                  </p>

                  <button
                    className="mt-6 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl transition"
                  >
                    Open →
                  </button>

                </div>

              </div>

            ))}

          </div>

          {/* Footer */}

          <div className="mt-12 bg-white rounded-3xl shadow-md p-6 text-center">

            <h3 className="text-xl font-semibold text-green-700">

              🌿 Plant Tip of the Day

            </h3>

            <p className="text-gray-600 mt-3">

              Always check the soil moisture before watering.
              Overwatering is one of the most common causes of plant damage.

            </p>

          </div>

        </div>

      </div>

    </div>

  );

}