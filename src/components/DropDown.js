import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 250,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  }
}));

export default function SimpleSelect({setcommand, selectedOptions, drop, setSelected}) {
  const classes = useStyles();
  const [gesture, setGesture] = React.useState('');

  const handleChange = (event) => {
    setGesture(event.target.value);
    setcommand(gesture);
  };

  return (
    <div className ="dropdowncolour"> {/* errrrr*/}
      <FormControl variant="outlined" className={classes.formControl}>
        <InputLabel id="demo-simple-select-outlined-label" color="secondary" > Select Gesture</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          

          value={gesture}
          onChange={handleChange}
          label="Gesture"
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>

          <MenuItem value={10}>Volume Mode</MenuItem>
          <MenuItem value={20}>Scroll</MenuItem>


        </Select>
      </FormControl>
    </div>
  );
}
