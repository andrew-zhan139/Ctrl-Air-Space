import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';
import ActionCommand from './ActionCommand';

import './index.scss';
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles"

const theme = createMuiTheme({
    palette: {
        type: "dark"
    }
});

// ReactDOM.render(<App />, document.getElementById('root'))

const rootElement = document.getElementById("root");
ReactDOM.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <App />
        </ThemeProvider>
    </React.StrictMode>,
    rootElement
);
