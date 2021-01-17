import React from 'react';
import { Button } from '@material-ui/core';

/*import logo from './example.png';*/


export default function ActionCommand() {

  return (
    <>
      <h1>Welcome to Swipe</h1>
      {/*<img src={logo} alt="logo" />*/} 
      <Button onClick={() => {
        electron.notificationApi.sendNotification('My custom notification sent from action command!');
      }}>Notify</Button>
    </>
  )
}