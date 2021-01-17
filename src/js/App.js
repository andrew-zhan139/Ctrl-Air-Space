import React from 'react';
import { Button } from '@material-ui/core';

import GestureMatcher from './components/GestureMatch';
import DropDown from './components/DropDown';
import OnOffSwitch from './components/OnOffSwitch';

import { makeStyles, useTheme } from "@material-ui/core/styles";
import ModificationTile from './components/ModificationTile';

export default function App() {

  const Actions = ["Open Window", "Close Window", "Volume Control"];
  const thepath1 = 'C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\components\\example.png';
  const thepath2 = "C:\\Users\\angel\\Downloads\\Swipe\\src\\js\\components\\onefinger.jpg";

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
      <ModificationTile className="modification-indv-tile" thepath={thepath1} actionName={'action sample 1'} actionDescription={'action description 1'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath1} actionName={'action sample 2'} actionDescription={'action description 2'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath2} actionName={'action sample 3'} actionDescription={'action description 3'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath1} actionName={'action sample 4'} actionDescription={'action description 4'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath2} actionName={'action sample 5'} actionDescription={'action description 5'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath1} actionName={'action sample 6'} actionDescription={'action description 6'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath2} actionName={'action sample 7'} actionDescription={'action description 7'}/>
      <ModificationTile className="modification-indv-tile" thepath={thepath1} actionName={'action sample 8'} actionDescription={'action description 8'}/> </div>
      <div>
        <OnOffSwitch />
      </div>
      <Button variant="contained" color="primary" onClick={() => {
        electron.notificationApi.sendNotification('Your gesture preferences have been updated.');
      }}>Save Preferences</Button>
      
    </>
  )
}
