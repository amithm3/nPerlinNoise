import "./PyLink.css";
import {Component} from "react";
import "https://cdn.jsdelivr.net/pyodide/v0.21.2/full/pyodide.js";
// import {loadPyodide} from 'pyodide';

export default class PyLink extends Component {
    static defaultProps = {
        pkgs: []
    }

    constructor(props) {
        super(props);
        this.state = {doneSetup: false};
    }

    async setup() {
        let ts = Date.now();
        this.pyLink = await window.loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.21.2/full"
        });
        await this.loadPkgs(this.props.pkgs);
        await this.loadZip(require("./src.zip"));
        await this.loadPy(require("./py_entry.py"));
        ts = Date.now() - ts;
        console.log("PyLink Setup Complete", ts, "ms");
        this.setState({doneSetup: true});
    }

    componentDidMount() {
        if (!this.props.noSetupOnLoad) this.setup().then();
    }


    runScript(script) {
        this.pyLink.runPython(script);
    }

    getFoo(foo) {
        foo = this.pyLink.runPython(foo);

        function wrap({args, kwargs} = {args: [], kwargs: {}}) {
            let rVal = foo.callKwargs(...args, kwargs);
            if (rVal) console.log(rVal)
        }

        return wrap;
    }

    async loadZip(file, type = 'zip', to = './src') {
        this.pyLink.unpackArchive(await (await fetch(file)).arrayBuffer(), type, {extractDir: to});
    }

    // file -> require(fpath)
    async loadPy(file) {
        let script = await (await fetch(file)).text();
        this.runScript(script);
    }

    async loadPkgs(names) {
        await this.pyLink.loadPackage(names);
    }

    render() {
        return (
            <div className="PyLink">
                {this.state.doneSetup ? "Use the console to see the results" : "PyLink Loading..."}<br/>
                <button onClick={() => this.getFoo("fooPrint")()}>console log from python</button>
                <br/>
                <button onClick={() => this.getFoo("fooArgsNoReturn")({
                        args: [420, 69.69, "Foo wo", true, null, undefined, NaN],
                        kwargs: {
                            list: [1, 1.1, "loo", false],
                            dict: {"m1": 1, "m2": 2.2, "m3": "moo", "m4": null},
                            num: 73,
                        }
                    }
                )}>
                    send args and kwargs (no return) to python
                </button>
                <br/>
                <button onClick={() => this.getFoo("fooWithReturn")({
                        args: [420, 69.69, "Foo wo", true, null, undefined, NaN],
                        kwargs: {
                            list: [1, 1.1, "loo", false],
                            dict: {"m1": 1, "m2": 2.2, "m3": "moo", "m4": null},
                            num: 73,
                        }
                    }
                )}>
                    send args and kwargs (with return) to python
                </button>
            </div>
        );
    }
}
