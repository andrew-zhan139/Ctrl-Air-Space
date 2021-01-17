import React from "react";

class GestureMatcher extends React.Component {
    render () {
        return (
            <header className="Gesture-Matcher">
                <div className = "card">
                        <img src="C:\Users\angel\Downloads\Swipe\src\js\components\CTRLALTSPACE.png" alt="Ctrl+Air+Space Logo" />
                        <br></br>
                    <text className="gesture-matcher">Welcome to the settings: Set your corresponding action and air gesture preferences here to be saved.</text>
                    <br></br>
                    <br></br>
                    <h1>Actions</h1>
                </div>
            </header>
        );
    }
}

export default GestureMatcher;