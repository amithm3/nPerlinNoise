import './Linp.css';
import {useState} from "react";

let guid = 0;

export default function LInp
    ({
         onInputBefore = () => null,
         onInput = () => null,
         labelMap = () => '',
         labelProps = {},
         inputProps = {},
         LInpProps = {},
         type = 'text',
         min = undefined,
         max = undefined,
         value = '',
     }) {
    const prefix = "LInpUIdPrefix--some-string-to-make-this-difficult-to-clash-with-user-defined-id" + guid++;
    const noVals = ['', NaN, null, undefined];
    const [value_, setValue] = useState(value);

    function onInput_(e) {
        onInputBefore(e);
        if (e.isPropagationStopped()) return;
        const [val, min_, max_] = ["number", "range"].includes(type) ?
            [parseInt(e.target.value), parseInt(min), parseInt(max)] :
            [e.target.value, min, max];
        let _val = val;
        const noVal = noVals.includes(val);
        if (noVal) _val = value_;
        if (noVal || ((noVals.includes(min_) || min_ <= val) && (noVals.includes(max_) || val <= max_))) setValue(_val);
        else _val = value_;
        e.target.value = _val;
        onInput(e);
    }

    const Tag = type !== "textBox" ? "input" : "textarea";
    const text = labelMap(value_)
    return (
        <div {...LInpProps} className="LInp">
            <label {...labelProps} htmlFor={prefix}>{text}</label>
            <Tag value={value_} type={type} onInput={onInput_} wrap="off"
                 id={prefix} {...inputProps} min={min} max={max}/>
        </div>
    );
}
