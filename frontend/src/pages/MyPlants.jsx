import { useEffect, useState } from "react";
import Sidebar from "../components/SideBar";
import Navbar from "../components/Navbar";
import API from "../services/api";


export default function MyPlants() {


  const [plants, setPlants] = useState([]);

  const [plantName, setPlantName] = useState("");
  const [nickname, setNickname] = useState("");

  const [sidebarOpen,setSidebarOpen] = useState(false);

  const [error,setError] = useState("");
  const [success,setSuccess] = useState("");



  const loadPlants = async()=>{

    try{

      const res = await API.get("/plants");

      setPlants(res.data);


    }catch(err){

      console.log(err);

      setError("Unable to load plants.");

    }

  };



  useEffect(()=>{

    loadPlants();

  },[]);






  const addPlant = async()=>{


    if(!plantName.trim()){

      setError("Please enter plant name.");

      return;

    }


    try{


      setError("");

      await API.post("/plants",{

        plant_name:plantName,

        nickname:nickname

      });



      setPlantName("");

      setNickname("");

      setSuccess("Plant added successfully 🌱");


      loadPlants();



    }catch(err){

      console.log(err);

      setError("Unable to add plant.");

    }


  };








  const deletePlant = async(id)=>{


    try{


      setError("");

      await API.delete(`/plants/${id}`);


      setPlants((prev)=>

        prev.filter((plant)=>plant.id !== id)

      );


      setSuccess("Plant deleted successfully.");



    }catch(err){


      console.log(err);


      setError(

        err.response?.data?.detail ||

        "Delete failed."

      );


    }


  };







return (


<div className="flex min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100">



<Sidebar

open={sidebarOpen}

setOpen={setSidebarOpen}

/>




<div className="flex-1 md:ml-4">



<div className="p-4 md:p-8">



<Navbar

setSidebarOpen={setSidebarOpen}

/>

{/* HEADER */}


<div className="mt-4 bg-gradient-to-r from-green-700 to-emerald-500 rounded-3xl p-6 md:p-10 text-white shadow-xl">


<h1 className="text-3xl md:text-5xl font-bold">

🪴 My Plant Garden

</h1>


<p className="mt-3 text-green-100 text-lg">

Manage your personal plant collection.

</p>


</div>


{/* ADD PLANT */}



<div className="bg-white rounded-3xl shadow-xl p-5 md:p-8 mt-8">



<h2 className="text-2xl font-bold text-gray-800">

Add New Plant

</h2>



<div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-6">



<input

className="border border-green-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-green-500 outline-none"

placeholder="🌱 Plant Name"

value={plantName}

onChange={(e)=>setPlantName(e.target.value)}

/>




<input

className="border border-green-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-green-500 outline-none"

placeholder="🏷 Nickname"

value={nickname}

onChange={(e)=>setNickname(e.target.value)}

/>



</div>






<button

onClick={addPlant}

className="mt-6 w-full md:w-auto bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-xl font-semibold transition"

>


Add Plant

</button>





{
error &&

<p className="text-red-600 mt-4 font-medium">

{error}

</p>

}



{
success &&

<p className="text-green-600 mt-4 font-medium">

{success}

</p>

}





</div>








{/* PLANT CARDS */}



<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">



{

plants.map((plant)=>(



<div

key={plant.id}

className="bg-white rounded-3xl shadow-lg p-6 hover:shadow-2xl hover:-translate-y-1 transition"

>



<div className="flex justify-between items-center">


<div className="text-6xl">

🪴

</div>


<span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">

Plant

</span>


</div>





<h2 className="text-2xl font-bold mt-5 text-gray-800">

{plant.plant_name}

</h2>



<p className="text-gray-500 mt-1">

{plant.nickname || "No nickname"}

</p>





<div className="mt-6 space-y-3 text-gray-700">


<p>

☀ <b>Sunlight:</b> {plant.sunlight || "Unknown"}

</p>



<p>

💧 <b>Water:</b> {plant.watering_frequency || "Unknown"}

</p>



<p>

🧬 <b>Name:</b> {plant.scientific_name || "Unknown"}

</p>


</div>






<button

onClick={()=>deletePlant(plant.id)}

className="mt-6 w-full bg-red-500 hover:bg-red-600 text-white py-3 rounded-xl font-semibold transition"

>


Delete Plant

</button>





</div>



))


}







{
plants.length===0 &&


<div className="col-span-full bg-white rounded-3xl shadow p-10 text-center">


<div className="text-7xl">

🌱

</div>


<h2 className="text-2xl font-bold mt-4">

No Plants Added

</h2>


<p className="text-gray-500 mt-2">

Start building your personal garden.

</p>


</div>


}





</div>





</div>



</div>



</div>


);

}