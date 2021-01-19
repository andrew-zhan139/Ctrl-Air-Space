import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';

import './index.scss';
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles"

const theme = createMuiTheme({
    palette: {
        type: "dark"
    }
});

const rootElement = document.getElementById("root");
ReactDOM.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <App />
        </ThemeProvider>
    </React.StrictMode>,
    rootElement
);
