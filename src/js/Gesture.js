import React from 'react';
import { Button } from '@material-ui/core';


export default function Gesture() {

  return (
    <>
      <h1>Welcome to Swipe</h1>
      <Button onClick={() => {
        electron.notificationApi.sendNotification('My custom notification sent from gesture');
      }}>Notify</Button>
    </>
  )
}