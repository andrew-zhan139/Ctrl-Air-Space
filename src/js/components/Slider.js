import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

const useStyles = makeStyles({
  root: {
    width: 300,
  },
});

function valuetext(value) {
  return `${value}°C`;
}

export default function DiscreteSlider({setmouse, setscroll}) {
  const classes = useStyles();
  const scrollChange = (event) => {
    setscroll(event.target.value);
  };
  const mouseChange = (event) => {
    setmouse(event.target.value);
  };
  return (
    <div className={classes.root}>
      <Typography color="primary" gutterBottom variant="h5" component="h2">
            Scroll Sensitivity
      </Typography>
      <Slider
        onChange={scrollChange}
        defaultValue={5}
        getAriaValueText={valuetext}
        aria-labelledby="discrete-slider"
        valueLabelDisplay="auto"
        step={1}
        marks
        min={1}
        max={10}
      />
      <Typography color="primary" gutterBottom variant="h5" component="h2">
            Mouse Sensitivity
      </Typography>
      <Slider
        defaultValue={3}
        getAriaValueText={valuetext}
        onChange={mouseChange}
        aria-labelledby="discrete-slider"
        valueLabelDisplay="auto"
        step={1}
        marks
        min={1}
        max={5}
      />
    </div>
  );
}