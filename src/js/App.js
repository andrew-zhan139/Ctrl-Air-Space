import React, { useState } from 'react';
import { Button } from '@material-ui/core';
//import fs from 'fs';

import GestureMatcher from './components/GestureMatch';
import DropDown from './components/DropDown';
import OnOffSwitch from './components/OnOffSwitch';
import DiscreteSlider from './components/Slider';

import { makeStyles, useTheme } from "@material-ui/core/styles";
import ModificationTile from './components/ModificationTile';


const fs  = require('fs');
export default function App() {

  const Actions = ["Open Window", "Close Window", "Volume Control"];
  const thepath1 = "C:\\Users\\andre\\Swipe\\src\\js\\components\\example.png";
  const thepath2 = "C:\\Users\\andre\\Swipe\\src\\js\\components\\onefinger.jpg";
  const [selectedOptions, setSelected] = useState([]);  
  const [peace, setPeace] = useState("");
  const [rock, setRock] = useState("");
  const [mousesen, setmouse] = useState();
  const [scrollsen, setscroll] = useState();
 
  let data = `{"Rock":${rock}, "Peace":${peace}, "MouseSensitivity":${mousesen}, "ScrollSensitivity":${scrollsen}}`;
  
return (
    <>
      <h1>Ctrl+Air.Space</h1>
      <h2></h2>
      <GestureMatcher />
      {/*<div className="gestures">
        <DropDown />
        <DropDown />
        <DropDown />
        <DropDown />
        <DropDown />
        <DropDown />
  </div>*/}
  <div className="modification-tiles">
      <ModificationTile setcommand={setRock} set={"Mouse Movement"} theges={"Palm"} setSelected={setSelected} thepath={thepath1} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} set={"Click"} theges={"Palm Open, Palm Close"} setSelected={setSelected} thepath={thepath1} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} set={2} theges={"Rock"} setSelected={setSelected} thepath={thepath2} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setPeace} set={2} theges={"Peace"} setSelected={setSelected} thepath={thepath1} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} set={"Change Tabs"} theges={"Slap"} setSelected={setSelected} thepath={thepath2} selectedOptions={selectedOptions}/>
      <ModificationTile setcommand={setRock} set={"Speech Input"} theges={"Call"}setSelected={setSelected} thepath={thepath1} selectedOptions={selectedOptions}/>
      </div>
      <div>
        <DiscreteSlider setscroll={setscroll} setmouse={setmouse}/>
      </div>
      <Button variant="contained" color="primary" onClick={() => {
        electron.notificationApi.sendNotification('Your gesture preferences have been updated.');
        fs.writeFile('settingsfile.txt', data, (error) => {
          if (error) throw err; 
      })
      }}>Save Preferences</Button>
      <div>
        <OnOffSwitch />
      </div>
      
    </>
  )
}
