import { useState } from "react";
import axios from "axios";

function Upload() {

const [source, setSource] = useState("SAP");

const upload = async () => {

await axios.post(
"${API}/records/"
,
{
source
}
);

alert("Saved");

};

return (

<div>

<h1>Upload Data</h1>

<select
value={source}
onChange={(e)=>
setSource(
e.target.value
)}
>

<option>SAP</option>
<option>UTILITY</option>
<option>TRAVEL</option>

</select>

<button
onClick={upload}
>

Upload

</button>

</div>

);

}

export default Upload;