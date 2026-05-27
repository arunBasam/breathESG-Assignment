import { useState } from "react";
import axios from "axios";
import Dashboard from "./pages/Dashboard";

function App() {

const [source, setSource] =
useState("SAP");

const upload = async () => {

try {

await axios.post(
"http://127.0.0.1:8000/api/records/",
{
source
}
);

window.location.reload();

}

catch (err) {

if (
err?.response?.status === 409
) {

alert(
"Source already uploaded"
)

}

else {

alert(
"Upload failed"
)

}

}

};

return (

<div

style={{

background:"#070b18",

minHeight:"100vh",

color:"white"

}}

>

<div

style={{

display:"flex",

justifyContent:"center",

paddingTop:"40px"

}}

>

<div

style={{

background:"#101828",

padding:"24px",

borderRadius:"16px",

display:"flex",

alignItems:"center",

gap:"16px",

boxShadow:
"0 0 20px rgba(0,0,0,.3)"

}}

>

<h2

style={{
margin:0
}}

>

Upload Data

</h2>

<select

value={source}

onChange={(e)=>
setSource(
e.target.value
)
}

style={{

padding:"10px",

borderRadius:"8px",

width:"150px"

}}

>

<option>SAP</option>
<option>UTILITY</option>
<option>TRAVEL</option>

</select>

<button

onClick={upload}

style={{

padding:
"10px 20px",

borderRadius:
"8px",

background:
"#2563eb",

color:
"white",

border:
"none",

cursor:
"pointer"

}}

>

Upload

</button>

</div>

</div>

<div
style={{
marginTop:"40px"
}}
>

<Dashboard />

</div>

</div>

);

}

export default App;