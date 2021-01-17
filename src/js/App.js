import React from 'react';
import { Button } from '@material-ui/core';

import GestureMatcher from './components/GestureMatch';
import DropDown from './components/DropDown';
import OnOffSwitch from './components/OnOffSwitch';

import { makeStyles, useTheme } from "@material-ui/core/styles";
import ModificationTile from './components/ModificationTile';

export default function App() {

  const Actions = ["Open Window", "Close Window", "Volume Control"];
  
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
      <ModificationTile actionName={'action sample'}/>
      <ModificationTile />
      <ModificationTile />
      <ModificationTile />
      <ModificationTile />
      <ModificationTile />
      <ModificationTile />
      <ModificationTile /> </div>
      <div>
        <OnOffSwitch />
      </div>
      <Button variant="contained" color="primary" onClick={() => {
        electron.notificationApi.sendNotification('Your gesture preferences have been updated.');
      }}>Save Preferences</Button>
      
    </>
  )
}
