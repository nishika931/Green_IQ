import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../services/api";


export default function Search() {

  const [query, setQuery] = useState("");
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(false);

  const [selectedPlant, setSelectedPlant] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const [sidebarOpen,setSidebarOpen] = useState(false);

  const [error,setError] = useState("");



  const searchPlant = async () => {

    if (!query.trim()) return;

    setError("");
    setLoading(true);


    try {

      const res = await API.get(
        `/plant-info/search?q=${query}`
      );

      setPlants(res.data.data || []);


    } catch(err){

      console.log(err);

      setError(
        "Unable to search plants. Please try again."
      );

    }


    setLoading(false);

  };




  const viewDetails = async (plant)=>{


    try{

      setError("");

      const res = await API.post(
        "/plant-ai/details",
        {
          plant_name: plant.common_name
        }
      );


      setSelectedPlant(res.data);

      setShowModal(true);



    }catch(err){

      console.log(err);

      setError(
        "Unable to fetch plant details."
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

🔍 Plant Explorer

</h1>


<p className="mt-3 text-green-100 text-lg">

Discover plants and get AI powered care guides.

</p>


</div>






{/* SEARCH */}


<div className="bg-white rounded-3xl shadow-xl p-5 md:p-8 mt-8">


<h2 className="text-xl md:text-2xl font-bold text-gray-800">

Search Your Plant

</h2>



<div className="flex flex-col md:flex-row gap-4 mt-6">


<input

className="flex-1 border border-green-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-green-500 outline-none"

placeholder="🌱 Enter plant name..."

value={query}

onChange={(e)=>setQuery(e.target.value)}

/>



<button

onClick={searchPlant}

className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-xl font-semibold transition"

>

Search

</button>



</div>


{
error &&

<p className="text-red-600 mt-4 font-medium">

{error}

</p>

}



</div>







{
loading &&

<div className="text-center mt-10">


<div className="animate-spin text-4xl">

🌿

</div>


<p className="text-gray-600 mt-3">

Searching plants...

</p>


</div>

}







{/* CARDS */}


<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">


{
plants.map((plant)=>(


<div

key={plant.id}

className="bg-white rounded-3xl shadow-lg overflow-hidden hover:-translate-y-1 hover:shadow-2xl transition"


>


<img

src={
plant.default_image?.medium_url ||
"https://placehold.co/500x300?text=Plant"
}

alt={plant.common_name}

className="w-full h-52 object-cover"

/>



<div className="p-6">


<h2 className="text-2xl font-bold text-gray-800">

{plant.common_name}

</h2>



<p className="italic text-gray-500 mt-2">

{plant.scientific_name?.[0]}

</p>




<button

onClick={()=>viewDetails(plant)}

className="w-full mt-6 bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold transition"

>

View AI Care Guide

</button>



</div>


</div>



))

}



</div>





{
!loading && plants.length===0 &&

<div className="mt-10 bg-white rounded-3xl shadow p-10 text-center">


<div className="text-6xl">

🌱

</div>


<h2 className="text-2xl font-bold mt-4">

Search plants to explore

</h2>


<p className="text-gray-500 mt-2">

Find information about thousands of plants.

</p>


</div>

}





</div>


</div>









{/* MODAL */}


{
showModal && selectedPlant &&


<div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">


<div className="bg-white rounded-3xl w-full max-w-4xl max-h-[90vh] overflow-y-auto p-6 md:p-8 shadow-2xl">


<button

onClick={()=>setShowModal(false)}

className="float-right text-2xl"

>

✖

</button>



<img

src={
selectedPlant.basic_info.image ||
"https://placehold.co/700x400?text=Plant"
}

className="w-full h-60 md:h-72 object-cover rounded-2xl"

/>




<h1 className="text-3xl md:text-4xl font-bold text-green-700 mt-6">

{selectedPlant.basic_info.common_name}

</h1>



<p className="italic text-gray-500 mt-2">

{selectedPlant.basic_info.scientific_name.join(", ")}

</p>




<div className="mt-8 bg-green-50 rounded-2xl p-5 leading-8">


{selectedPlant.ai_care_guide}


</div>



</div>


</div>


}



</div>


);

}