import React, { useState } from 'react';
import { Button } from '@material-ui/core';
//import fs from 'fs';
//import fs from 'fs';
import GestureMatcher from './components/GestureMatch';
import DropDown from './components/DropDown';
import OnOffSwitch from './components/OnOffSwitch';
import DiscreteSlider from './components/Slider';

import { makeStyles, useTheme } from "@material-ui/core/styles";
import ModificationTile from './components/ModificationTile';
//import {fs} from 'fs';
function processSayingHi() { 
  var xhr = new XMLHttpRequest();
xhr.open("GET", "http://127.0.0.1:5000/hello", true);
xhr.responseType = "text";
xhr.onload = function(e) {
  console.log(xhr.response);
}
xhr.send();
console.log(xhr.responseText);

}
//const fs = require('fs');
export default function App() {
  
  const Actions = ["Open Window", "Close Window", "Volume Control"];

  const thepath1 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\MotionGIFS\\palm.gif";
  const thepath2 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\MotionGIFS\\squeeze.gif";
  const thepath3 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\MotionGIFS\\spiderman.gif";
  const thepath4 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\MotionGIFS\\scroll.gif";
  const thepath5 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\MotionGIFS\\slap.gif";
  const thepath6 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\MotionGIFS\\call.gif";

  const [selectedOptions, setSelected] = useState([]);  
  const [peace, setPeace] = useState("");
  const [rock, setRock] = useState("");
  const [mousesen, setmouse] = useState();
  const [scrollsen, setscroll] = useState();
 
  //let data = `{"Rock":${rock}, "Peace":${peace}, "MouseSensitivity":${mousesen}, "ScrollSensitivity":${scrollsen}}`;
  
return (

    <>
      <GestureMatcher />

  <div className="modification-tiles">
      <ModificationTile setcommand={setRock} className="modification-indv-tile" set={"Mouse Movement"} theges={"Palm"} gestureDescription={"Move palm to control the mouse"} setSelected={setSelected} thepath={thepath1} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} className="modification-indv-tile"set={"Click"} theges={"Palm Open, Palm Close"} gestureDescription={"Go from open to close palm to click"} setSelected={setSelected} thepath={thepath2} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} className="modification-indv-tile" set={2} theges={"Rock"} gestureDescription={"Do the rock sign to perform associated action"} setSelected={setSelected} thepath={thepath3} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setPeace} className="modification-indv-tile" set={2} theges={"Peace"} gestureDescription={"Do the peace sign to perform associated action"} setSelected={setSelected} thepath={thepath4} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} className="modification-indv-tile" set={"Change Tabs"} gestureDescription={""} theges={"Swipe"} gestureDescription={"Perform horizontal swipe to switch between two windows and vertical swipe to shift between all windows"} setSelected={setSelected} thepath={thepath5} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} className="modification-indv-tile" set={"Speech Input"} theges={"Call"} gestureDescription={"Make call sign to activate voice input"} setSelected={setSelected} thepath={thepath6} selectedOptions={selectedOptions}/>
      </div>

      <div>
        <DiscreteSlider setscroll={setscroll} setmouse={setmouse}/>
      </div>
      <Button variant="contained" color="primary" onClick={() => {

        electron.notificationApi.sendNotification('Your gesture preferences have been updated.');
        processSayingHi();
        //fs.writeFile('settingsfile.txt', data, (error) => {
      //    if (error) throw err; 
     // })
      }}>Save Preferences and Start</Button>
      <div>
      </div>

      
    </>
  )
}
