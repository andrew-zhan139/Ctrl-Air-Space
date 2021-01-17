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
    minWidth: 200,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  }
}));

export default function SimpleSelect(prop) {
  const classes = useStyles();
  const [gesture, setGesture] = React.useState('');

  const handleChange = (event) => {
    setGesture(event.target.value);
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
          <MenuItem value={10}>Fist</MenuItem>
          <MenuItem value={20}>Call</MenuItem>
          <MenuItem value={30}>Pinch</MenuItem>
          <MenuItem value={40}>Flat</MenuItem>
          <MenuItem value={50}>Closed-Palm</MenuItem>
          <MenuItem value={60}>Open-Palm</MenuItem>
        </Select>
      </FormControl>
    </div>
  );
}
