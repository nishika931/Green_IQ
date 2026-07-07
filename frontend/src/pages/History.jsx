import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../services/api";
import { useNavigate } from "react-router-dom";


export default function History() {

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen,setSidebarOpen] = useState(false);


  useEffect(() => {

    loadHistory();

  }, []);



  const loadHistory = async () => {

    try {

      const res = await API.get("/chat/history");

      console.log("History:", res.data);

      setHistory(res.data);

    } catch (err) {

      console.log("History Error:", err.response?.data || err.message);

    }

    setLoading(false);

  };


  return (

    <div className="flex min-h-screen bg-[#F5FBF6]">

      <Sidebar 
      open={sidebarOpen}
      setOpen={setSidebarOpen}
      />


      <main className="flex-1 md:ml-4">

        <div className="p-4 md:p-8">


          {/* Navbar */}

          <Navbar
          setSidebarOpen={setSidebarOpen}
          />



          {/* Page Header */}

          <div className="mt-4 bg-white rounded-3xl shadow-lg p-6 md:p-8">


            <h1 className="text-3xl font-bold text-green-700">

              💬 Chat History

            </h1>


            <p className="text-gray-500 mt-2">

              Your previous conversations with Plant Doctor AI.

            </p>


          </div>




          {loading && (

            <div className="mt-8 bg-white rounded-3xl p-8 text-center shadow">

              Loading conversations...

            </div>

          )}





          {!loading && history.length === 0 && (

            <div className="mt-8 bg-white rounded-3xl p-10 text-center shadow">


              <div className="text-6xl">

                🌿

              </div>


              <h2 className="text-2xl font-bold mt-4">

                No conversations yet

              </h2>


              <p className="text-gray-500 mt-2">

                Start chatting with Plant Doctor to create history.

              </p>


            </div>

          )}






          {!loading && history.length > 0 && (

            <div className="mt-8 space-y-5">


              {history.map((chat)=>(


                <div

                  key={chat.id}

                  className={`max-w-3xl rounded-3xl p-5 shadow-lg ${
                    
                    chat.role === "user"

                    ? "bg-green-600 text-white ml-auto"

                    : "bg-white border"

                  }`}

                >


                  <h3 className="font-bold mb-3">

                    {chat.role === "user"

                    ? "🧑 You"

                    : "🌿 Plant Doctor"}

                  </h3>


                  <p className="whitespace-pre-wrap">

                    {chat.message}

                  </p>


                  <p className="text-xs mt-4 opacity-70">

                    {new Date(chat.created_at).toLocaleString()}

                  </p>


                </div>


              ))}


            </div>

          )}



        </div>

      </main>


    </div>

  );

}