import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

const API =
import.meta.env.VITE_API_URL

function Dashboard() {

const [rows, setRows] = useState([]);
const [loading, setLoading] = useState(false);
const [lastRefresh, setLastRefresh] = useState("");
const [page, setPage] = useState(1);

const rowsPerPage = 5;

const [search, setSearch] =
useState("");

const [filter, setFilter] =
useState("ALL");

const [statusFilter,
setStatusFilter] =
useState("ALL");

const [sortBy,setSortBy]=
useState("id");

const [sortOrder,setSortOrder]=
useState("desc");

const [selectedId,
setSelectedId]
=
useState(
null
);

const load = async () => {

try {

setLoading(true);

const res =
await axios.get(
`${API}/records/list/`
)

setRows(

res.data.data.sort(
(a,b)=>b.id-a.id
)

);

setLastRefresh(
new Date()
.toLocaleTimeString()
);
}

catch {

toast.error(
"Unable to load records"
);

}

finally {

setLoading(false);

}

};

useEffect(()=>{

load();

setPage(
1
);

const interval =

setInterval(()=>{

load();

},10000);

return ()=>{

clearInterval(
interval
);

};

},[]);

const sort = (column)=>{

if(sortBy===column){

setSortOrder(

sortOrder==="asc"

?

"desc"

:

"asc"

);
setPage(1);
}

else{

setSortBy(column);

setSortOrder("asc");

setPage(1);
}

};

const exportCSV = ()=>{

const headers =

[
"ID",
"Source",
"Type",
"Scope",
"Status",
"Suspicious",
"Uploaded"
];

const csv = [

headers.join(","),

...filteredRows.map((r)=>

[

r.id,

r.source,

r.source_type,

r.scope,

r.status,

r.suspicious

?

"Review"

:

"Clean",

r.uploaded_at

]

.join(",")

)

].join("\n");

const blob =

new Blob(
[csv],
{
type:
"text/csv"
}
);

const url =
URL.createObjectURL(
blob
);

const link =

document.createElement(
"a"
);

link.href =
url;

link.download =

"records.csv";

link.click();

URL.revokeObjectURL(
url);

};

const approve = async(id)=>{

try{

await axios.post(
`${API}/records/${id}/approve/`
);

toast.success(
"Record approved"
);

await load();


}

catch {

toast.error(
"Approve failed"
);

}

};

const reject = async(id)=>{

try{

await axios.post(
`${API}/records/${id}/reject/`
);

toast.success(
"Record rejected"
);

await load();

}

catch {

toast.error(
"Reject failed"
);

}

};


const filteredRows =

rows

.filter((r)=>{

const sourceMatch =

filter==="ALL"

||

r.source===filter;

const searchMatch =

r.source

.toLowerCase()

.includes(
search.toLowerCase()
);

const statusMatch =

statusFilter==="ALL"

||

r.status===statusFilter;



return (

sourceMatch

&&

searchMatch

&&

statusMatch

);

})

.sort((a,b)=>{

let x=a[sortBy];
let y=b[sortBy];

if(sortBy==="uploaded_at"){

x=
new Date(x);

y=
new Date(y);

}

if(x<y)
return sortOrder==="asc"
?-1
:1;

if(x>y)
return sortOrder==="asc"
?1
:-1;

return 0;

});

const start =

(page - 1)

*

rowsPerPage;

const end =

start

+

rowsPerPage;

const paginatedRows =

filteredRows.slice(
start,
end
);

const totalPages =

Math.ceil(

filteredRows.length

/

rowsPerPage

);

useEffect(()=>{

if(

page

>

totalPages

&&

totalPages>0

){

setPage(
totalPages
);

}

},[totalPages]);

const total =
filteredRows.length;

const pending =
filteredRows.filter(
r=>r.status!=="LOCKED"
).length;

const suspicious =
filteredRows.filter(
r=>r.suspicious
).length;

const suspiciousRate =

total

?

Math.round(

(
suspicious
/

total

)

*

100

)

:

0;

const approvedRate =

total

?

Math.round(

(
filteredRows.filter(
r=>
r.status==="LOCKED"
).length
/

total

)

*

100

)

:

0;

return(

<div

style={{

maxWidth:"1200px",

margin:"40px auto",

color:"white"

}}

>

<h1

style={{

fontSize:"42px",

textAlign:"center"

}}

>

Analyst Review Dashboard

</h1>

<div
style={{
textAlign:"center"
}}
>

<button

onClick={async()=>{

await load();

}}

disabled={loading}

style={{

padding:"10px 24px",

borderRadius:"10px",

border:"none",

background:"#2563eb",

color:"white",

cursor:
loading
?
"not-allowed"
:
"pointer",

opacity:
loading
?
0.7
:
1,

marginTop:"10px"

}}

>

{

loading

?

"Loading..."

:

"Refresh"

}

</button>


<button

onClick={
exportCSV
}

style={{

marginLeft:"10px",

padding:"10px 20px",

border:"none",

borderRadius:"10px",

background:"#16a34a",

color:"white",

cursor:"pointer"

}}

>

Export CSV

</button>

<p
style={{
marginTop:"10px",
fontSize:"14px",
color:"#94a3b8"
}}
>

Last Updated:

{

lastRefresh

||

"Never"

}

</p>

</div>

<div

style={{

display:"flex",

justifyContent:"center",

gap:"15px",

margin:"30px"

}}

>

<input

placeholder="Search Source"

value={search}

onChange={(e)=>

setSearch(

e.target.value

)

}

style={{

padding:"12px",

width:"240px",

borderRadius:"8px"

}}

/>

<select

value={filter}

onChange={(e)=>

setFilter(

e.target.value

)

}

style={{

padding:"12px",

borderRadius:"8px"

}}

>

<option>ALL</option>
<option>SAP</option>
<option>UTILITY</option>
<option>TRAVEL</option>

</select>

<select

value={statusFilter}

onChange={(e)=>

setStatusFilter(
e.target.value
)

}

style={{

padding:"12px",

borderRadius:"8px"

}}

>

<option>
ALL STATUS
</option>

<option>
PENDING
</option>

<option>
LOCKED
</option>

</select>

<button

onClick={()=>{

setSearch("");

setFilter("ALL");

setStatusFilter(
"ALL"
);

}}

style={{

padding:"10px 16px",

background:"#374151",

color:"white",

border:"none",

borderRadius:"8px"

}}

>

Clear

</button>

</div>

<div

style={{

display:"flex",

justifyContent:"center",

gap:"24px",

margin:"30px 0"

}}

>

<Card
title="Total"
value={total}
color="#13254d"
/>

<Card
title="Pending"
value={pending}
color="#755600"
/>

<Card
title="Suspicious"
value={suspicious}
color="#751515"
/>

</div>


<div

style={{

display:"flex",

justifyContent:"center",

gap:"20px",

marginBottom:"25px"

}}

>

<div

style={{

background:"#0f172a",

padding:"18px 36px",

borderRadius:"1px"

}}

>

Approval Rate

<br/>

<b>

{approvedRate}%

</b>

</div>

<div

style={{

background:"#0f172a",

padding:"16px 24px",

borderRadius:"12px"

}}

>

Suspicious Rate

<br/>

<b>

{suspiciousRate}%

</b>

</div>

</div>

<div

style={{

textAlign:"center",

color:"#94a3b8",

fontSize:"15px",

marginBottom:"18px"

}}

>

Showing

{" "+filteredRows.length+" " }

 of

{" "+rows.length+" " }

 records

•

{

" "+totalPages+" "

}

pages

</div>



<div

style={{

display:"flex",

justifyContent:"center",

alignItems:"center",

gap:"14px",

marginBottom:"20px"

}}

>

<button

disabled={
page===1
}

onClick={()=>{

setPage(
page-1
);

}}

>

← Prev

</button>

<span>

Page

{page}

/

{totalPages}

</span>

<button

disabled={

page===totalPages

||

totalPages===0

}

onClick={()=>{

setPage(
page+1
);

}}

>

Next →

</button>

</div>

<div

style={{

background:"#111827",

padding:"20px",

borderRadius:"14px",

overflowX:"auto"

}}

>

<table

style={{

width:"100%",

borderCollapse:"collapse"

}}

>

<thead>

<tr>

<TH>
<span
onClick={()=>
sort("id")
}
style={{
cursor:"pointer"
}}
>
ID

{

sortBy==="id"

?

sortOrder==="asc"

?

" ↑"

:

" ↓"

:

" ↕"

}
</span>
</TH>
<TH>Source</TH>
<TH>Type</TH>
<TH>Scope</TH>
<TH>
Status
(
{
rows.filter(
r=>
r.status==="PENDING"
).length
}
)
</TH>

<TH>
Suspicious
(
{
rows.filter(
r=>
r.suspicious
).length
}
)
</TH>

<TH>
<span
onClick={()=>
sort("uploaded_at")
}
style={{
cursor:"pointer"
}}
>
Uploaded

{

sortBy==="uploaded_at"

?

sortOrder==="asc"

?

" ↑"

:

" ↓"

:

" ↕"

}
</span>
</TH>
<TH>Audit</TH>

<TH>Action</TH>

</tr>

</thead>

<tbody>

{

paginatedRows.length===0

?

<tr>

<td

colSpan="9"

style={{

padding:"50px",

color:"#94a3b8",

fontSize:"18px"

}}

>

No records found

</td>

</tr>

:

paginatedRows.map((r)=>(

<tr

key={r.id}

onClick={()=>

setSelectedId(
r.id
)

}

style={{

cursor:"pointer",

background:

selectedId===r.id

?

"#1e3a8a"

:

r.suspicious

?

"#221111"

:

"transparent"

}}

>

<TD>{r.id}</TD>

<TD>{r.source}</TD>

<TD>{r.source_type}</TD>

<TD>{r.scope}</TD>

<TD>

<span

style={{

padding:"8px 14px",

borderRadius:"20px",

background:

r.status==="LOCKED"

?

"#146c2e"

:

"#8a6900"

}}

>

{

r.status==="LOCKED"

?

"🔒 LOCKED"

:

"⏳ PENDING"

}

</span>

</TD>

<TD>

{

r.suspicious

?

"⚠️ Review"

:

"✅ Clean"

}

</TD>

<TD>

{r.uploaded_at}

</TD>

<TD>

{

r.audit==="APPROVED"

?

<div>

<div
style={{
fontWeight:"400",
color:"#22c55e"
}}
>

✅ Approved

</div>

<div
style={{
fontSize:"12px",
color:"#94a3b8",
marginTop:"4px"
}}
>

{
r.audit_time
}

</div>

</div>

:

"-"

}

</TD>

<TD>

<button

disabled={
r.status==="LOCKED"
}

onClick={() => {

const ok =
window.confirm(
"Approve this record?"
);

if(ok){

approve(
r.id
);

}

}}

>

{

r.status==="LOCKED"

?

"Approved"

:

"Approve"

}

</button>

<button

disabled={
r.status==="REJECTED"
}

onClick={() => {

const ok =
window.confirm(
"Reject this record?"
);

if(ok){

reject(
r.id
);

}

}}

style={{

marginLeft:"10px"

}}

>

{

r.status==="REJECTED"

?

"Rejected"

:

"Reject"

}

</button>

</TD>
AuditLog.objects.create(
    record=record,
    action="REJECTED"
)
</tr>

))

}

</tbody>

</table>

</div>

</div>

);

}

function Card({

title,
value,
color

}){

return(

<div

style={{

width:"180px",

height:"110px",

background:color,

borderRadius:"16px",

display:"flex",

flexDirection:"column",

justifyContent:"center",

alignItems:"center",

padding:"14px"

}}

>

<h3

style={{

margin:"0",

fontSize:"22px"

}}

>

{title}

</h3>

<h1

style={{

marginTop:"8px",

fontSize:"44px"

}}

>

{value}

</h1>

</div>

);

}

function TH({children}){

return(

<th

style={{

padding:"18px"

}}

>

{children}

</th>

);

}

function TD({children}){

return(

<td

style={{

padding:"18px",

textAlign:"center"

}}

>

{children}

</td>

);

}

export default Dashboard;