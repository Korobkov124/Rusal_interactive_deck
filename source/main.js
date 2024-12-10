

const apiUrl = 'http://127.0.0.1:5000/users';
const data = {
    "id": 3,
    "name": "test2",
    "username": "test2",
    "tg": "@test2",
    "number": "+7(777)777-77-77",
    "email": "test2@test.ru",
    "password": "test2"
}
let login = 'admin';
let password = 'admin';
let response = await fetch(apiUrl, {headers: {Authorization: 'Basic ' + btoa(login + ':' + password)} });
if (!response.ok) {
  console.log(response);
  return 0;
}

const requestOptions = {

  method: 'POST',
  headers: {
    credentials: 'include',
    Authorization: 'Basic ' + btoa(login + ':' + password),
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
};

let response = await fetch(apiUrl,  requestOptions);
if (response.ok) {
  let json = await response.json();
  json = json["response"]
  if (json == "ok"){
    console.log("ok");
  }
  else {
  // console.log(json[0]);
  for (let i = 0; i < json.length; i++) {
    let sd = new Date(Date.parse(json[i]["time_start"]));
    let ed = new Date(Date.parse(json[i]["time_end"]));
    console.log(sd, ed);
  }
}
  

} else {
  console.log(response);
}