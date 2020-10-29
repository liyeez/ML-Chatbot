
import API from './api.js';
const api_dentist = new API('http://localhost:8080'); //change if port different 
const api_timeslot = new API('http://localhost:8081'); 

// 2 REST API 

setupEventListeners();
console.log("say hi");
export function setupEventListeners(){
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
          console.log(document.getElementsByTagName('textarea')[0].value);
          var userMsg = document.getElementsByTagName('textarea')[0].value;
          createDialogBox(userMsg, "useravatar.png");
        }
      });
      
}

// <div class="container">
//             <img src="useravatar.png" alt="Avatar" style="width:100%;">
//             <p>Hello. How are you today?</p>
//             <span class="time-right">11:00</span>
//           </div>
function createDialogBox(userMsg, avatar_link){
    var container = document.createElement('div');
    container.setAttribute("class", "container");
    
    var img = document.createElement("img");
    img.setAttribute("src", avatar_link);
    img.setAttribute("alt", "Avatar");
    img.style.width = "100%";

    var p = document.createElement("p");
    p.innerText = userMsg;

    var span = document.createElement("span");
    span.setAttribute("class", "time-right");
    span.innerText = new Date().toLocaleString().replace(',','');

    container.appendChild(img);
    container.appendChild(p);
    container.appendChild(span);

    document.getElementById("dialog").appendChild(container);
}

