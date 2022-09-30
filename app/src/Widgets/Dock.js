import "./Dock.css"
import LInp from "../components/LInp/LInp";

export default function () {
    return (
        <div className="Dock">
            <LInp type="number" min={2} max={32} value={2} step={1}
                  labelMap={() => "Frequency: "}
                  labelProps={{style: {display: 'initial'}}}/>
            <LInp type="range" min={1} max={8} value={8} step={1}
                  labelMap={val => "Octave(s): " + val + " "}/>
        </div>
    );
}
