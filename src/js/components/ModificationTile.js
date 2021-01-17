import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import DropDown from '../components/DropDown.js';

// import SimpleSelect from 'DropDown'

const useStyles = makeStyles({
  root: {
    maxWidth: 345,
  },
  media: {
    height: 140,
  },
});

export default function MediaCard({setcommand, set, theges, thepath, selectedOptions, drop, setSelected}) {
  const classes = useStyles();
  return (
    <Card className={classes.root}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="440"
          width="140"
          src={thepath}
          title="Finger"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            {theges}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Gesture action description.
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        {(set === 2)? <DropDown setcommand={setcommand} selectedOptions={selectedOptions} drop={drop} setSelected={setSelected}/>: <Typography variant="standard" color="textSecondary" component="p">    {set}</Typography>}
        
        </CardActions>
    </Card>
  );
}