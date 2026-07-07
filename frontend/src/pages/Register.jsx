import { useState } from "react";
import { Link,useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register(){

const {register}=useAuth();

const navigate=useNavigate();

const[username,setUsername]=useState("");
const[email,setEmail]=useState("");
const[password,setPassword]=useState("");
const [error, setError] = useState("");
const [success, setSuccess] = useState("");

const submit = async () => {

  try {

    setError("");
    setSuccess("");

    await register(username,email,password);

    setSuccess("Registration Successful!");

    setTimeout(() => {
      navigate("/");
    }, 1000);

  }

  catch(err){

    setError(
      err.response?.data?.detail || "Registration Failed"
    );

  }

};

return(

<div className="min-h-screen bg-gradient-to-br from-green-100 via-white to-green-200 flex items-center justify-center">

<div className="bg-white rounded-[35px] shadow-2xl grid lg:grid-cols-2 max-w-5xl w-full overflow-hidden">

<div className="hidden lg:flex bg-green-600 justify-center items-center flex-col text-white">

<div className="text-8xl">

🌿

</div>

<h1 className="text-5xl font-bold mt-6">

Green IQ

</h1>

</div>

<div className="p-10">

<h2 className="text-4xl font-bold">

Create Account

</h2>

<input

className="w-full p-4 border rounded-2xl mt-8"

placeholder="Username"

value={username}

onChange={(e)=>setUsername(e.target.value)}

/>

<input

className="w-full p-4 border rounded-2xl mt-5"

placeholder="Email"

value={email}

onChange={(e)=>setEmail(e.target.value)}

/>

<input

type="password"

className="w-full p-4 border rounded-2xl mt-5"

placeholder="Password"

value={password}

onChange={(e)=>setPassword(e.target.value)}

/>

<button

onClick={submit}

className="w-full bg-green-600 hover:bg-green-700 transition mt-8 rounded-2xl text-white p-4"

>

Register

</button>


{error && (

<p className="mt-4 text-center text-red-500 font-medium">

{error}

</p>

)}


{success && (

<p className="mt-4 text-center text-green-600 font-medium">

{success}

</p>

)}
<p className="text-center mt-5">

Already have an account?

<Link

to="/"

className="text-green-700 ml-2"

>

Login

</Link>

</p>

</div>

</div>

</div>

);

}