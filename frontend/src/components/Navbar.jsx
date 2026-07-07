import { Menu } from "lucide-react";

export default function Navbar({ setSidebarOpen, showGreeting=false }) {

  const user = JSON.parse(localStorage.getItem("user"));

  const hour = new Date().getHours();

  let greeting = "Good Evening";

  if(hour < 12){
    greeting = "Good Morning";
  }
  else if(hour < 18){
    greeting = "Good Afternoon";
  }


  return (

    <div className="flex items-center justify-between py-4">


      {/* Mobile Menu */}

      <button

        onClick={() => setSidebarOpen(true)}

        className="md:hidden p-2 rounded-lg hover:bg-green-100"

      >

        <Menu size={28}/>

      </button>



      {
        showGreeting && (

        <div className="flex-1 text-center">


          <h2 className="text-3xl md:text-5xl font-bold text-gray-800">

            {greeting} 👋

          </h2>


          <p className="text-gray-500 mt-2">

            Welcome back,

            <span className="text-green-700 font-semibold">

              {" "}{user?.username}

            </span>

          </p>


        </div>

        )
      }


    </div>

  );

}