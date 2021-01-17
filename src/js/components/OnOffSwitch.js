import React from 'react';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';

export default function SwitchLabels() {
  const [state, setState] = React.useState({
    enabled: true,
  });

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  return (
    <FormGroup row>
      <FormControlLabel
        control={<Switch inputProps={{ 'aria-label': 'primary checkbox' }}
          checked={state.enabled} onChange={handleChange} name="enabled" />}
        label="Enable Gestures"
        labelPlacement = "start"
      />
    </FormGroup>
  );
}
