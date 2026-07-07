import { useState, useRef, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../services/api";
import { useNavigate } from "react-router-dom";


export default function Doctor() {

 const [message, setMessage] = useState("");
 const [city, setCity] = useState("");
 const [loading, setLoading] = useState(false);
 const [messages, setMessages] = useState([]);
 const [error, setError] = useState("");
 const [sidebarOpen,setSidebarOpen] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  const suggestions = [
  "🍂 My leaves are turning yellow",
  "💧 Should I water my plant today?",
  "🐛 My plant has insects",
  "🌿 Brown spots on leaves"
];

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMessage = {
      role: "user",
      message
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {

      const res = await API.post("/chat", {
        message,
        city
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          message: res.data.response
        }
      ]);

      setMessage("");

    } catch (err) {

  console.log("CHAT ERROR:", err.response);

  setError(
    err.response?.data?.detail ||
    "Unable to contact Plant Doctor. Please try again."
  );

}
    setLoading(false);

  };

  return (

    <div className="flex min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100">

      <Sidebar 
open={sidebarOpen}
setOpen={setSidebarOpen}
/>


      <div className="flex-1 md:ml-4">

        <div className="max-w-7xl mx-auto p-4 md:p-8 pb-8 pt-2">

          <Navbar
setSidebarOpen={setSidebarOpen}
/>

          {/* Hero */}

          <div className="mt-2 rounded-3xl bg-gradient-to-r from-green-700 via-green-600 to-emerald-500 text-white shadow-xl overflow-hidden">

            <div className="p-6 md:p-8">

              <p className="uppercase tracking-[4px] text-sm text-green-100">

                AI Plant Assistant

              </p>

              <h1 className="text-4xl md:text-5xl font-bold mt-3">

                🩺 Plant Doctor

              </h1>

              <p className="mt-4 max-w-2xl text-green-100 leading-7">

                Ask anything about watering, diseases,
                sunlight, fertilizer, pests and plant care.

              </p>

            </div>

          </div>

          {/* Suggestions */}

          <div className="mt-8">

            <h3 className="font-semibold text-gray-700 mb-4">

              Quick Questions

            </h3>

            <div className="flex flex-wrap gap-3">

              {suggestions.map((item, index) => (

                <button
                  key={index}
                  onClick={() => setMessage(item)}
                  className="bg-white border border-green-100 rounded-full px-5 py-3 shadow hover:bg-green-50 hover:border-green-500 transition"
                >

                  {item}

                </button>

              ))}

            </div>

          </div>

          {/* Chat Container */}

          <div className="mt-8 bg-white rounded-3xl shadow-xl border border-green-100 overflow-hidden">
            /* Header */

            <div className="border-b px-6 py-5">

              <h2 className="text-2xl font-bold text-gray-800">

                🌿 AI Conversation

              </h2>

              <p className="text-gray-500 mt-1">

                Chat with your Plant Doctor

              </p>

            </div>

            {/* Messages */}

            <div className="h-[500px] overflow-y-auto p-6 space-y-6">

              {messages.length === 0 && (

                <div className="flex flex-col justify-center items-center h-full text-center">

                  <div className="text-7xl">

                    🌱

                  </div>

                  <h2 className="text-3xl font-bold mt-6">

                    Start Your Conversation

                  </h2>

                  <p className="text-gray-500 mt-3 max-w-lg">

                    Describe your plant problem and Green IQ AI
                    will help you diagnose and solve it.

                  </p>

                </div>

              )}

              {messages.map((chat, index) => (
                                <div
                  key={index}
                  className={`flex ${
                    chat.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >

                  <div
                    className={`flex gap-3 max-w-[85%] ${
                      chat.role === "user"
                        ? "flex-row-reverse"
                        : ""
                    }`}
                  >

                    {/* Avatar */}

                    <div
                      className={`w-11 h-11 rounded-full flex items-center justify-center shadow-md flex-shrink-0 ${
                        chat.role === "user"
                          ? "bg-green-600 text-white"
                          : "bg-green-100"
                      }`}
                    >

                      {chat.role === "user" ? "🧑" : "🌿"}

                    </div>

                    {/* Message */}

                    <div
                      className={`rounded-3xl px-5 py-4 whitespace-pre-wrap shadow-md leading-7 ${
                        chat.role === "user"
                          ? "bg-green-600 text-white rounded-tr-lg"
                          : "bg-green-50 border border-green-200 rounded-tl-lg text-gray-700"
                      }`}
                    >

                      <p className="font-semibold mb-2">

                        {chat.role === "user"
                          ? "You"
                          : "Plant Doctor"}

                      </p>

                      {chat.message}

                    </div>

                  </div>

                </div>

              ))}

              {loading && (

                <div className="flex">

                  <div className="flex gap-3">

                    <div className="w-11 h-11 rounded-full bg-green-100 flex items-center justify-center">

                      🌿

                    </div>

                    <div className="bg-green-50 border border-green-200 rounded-3xl rounded-tl-lg px-5 py-4">

                      <div className="flex gap-2">

                        <span className="w-2 h-2 rounded-full bg-green-600 animate-bounce"></span>

                        <span className="w-2 h-2 rounded-full bg-green-600 animate-bounce [animation-delay:150ms]"></span>

                        <span className="w-2 h-2 rounded-full bg-green-600 animate-bounce [animation-delay:300ms]"></span>

                      </div>

                    </div>

                  </div>

                </div>

              )}

              <div ref={bottomRef}></div>

            </div>

            {/* Input Area */}

            <div className="border-t bg-gray-50 p-6">

              <div className="grid md:grid-cols-4 gap-4">

                <input
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="📍 City (Optional)"
                  className="md:col-span-1 border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                />

                <textarea
                  rows={1}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => {

                    if (e.key === "Enter" && !e.shiftKey) {

                      e.preventDefault();

                      sendMessage();

                    }

                  }}
                  placeholder="Describe your plant problem..."
                  className="md:col-span-3 border rounded-xl px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-green-500"
                />

              </div>
              {error && (
  <p className="text-red-600 text-sm mb-4 font-medium">
    {error}
  </p>
)}

              <div className="flex flex-col md:flex-row justify-between items-center mt-5 gap-4">


                <button
                  onClick={sendMessage}
                  disabled={loading}
                  className="w-full md:w-auto bg-gradient-to-r from-green-600 to-emerald-500 hover:from-green-700 hover:to-emerald-600 disabled:opacity-50 text-white px-8 py-3 rounded-xl font-semibold transition"
                >

                  {loading ? "Thinking..." : "🌿 Ask AI Doctor"}

                </button>

              </div>

            </div>
                      </div>

        </div>

      </div>

    </div>

  );

}