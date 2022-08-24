import Canvas from "./canvas"
import Dock from "./dock"
import {Nav, Foo} from "./Nav&Foo"
import './App.css'

function App() {
    return (
        <>
            <Nav/>
            <div className="App">
                <Canvas/>
                <Dock/>
            </div>
            <Foo/>
        </>
    )
}

export default App;
