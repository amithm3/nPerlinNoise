import './DImg.css';
import {Component, createRef} from "react";

export default class DImg extends Component {
    static defaultProps = {
        width: 250,
        height: 250
    }

    constructor(props) {
        super(props);
        if (this.props.this) this.props.this.ref = this;
        this.canvasRef = createRef();
    }

    componentDidMount() {
        this.context = this.canvasRef.current.getContext('2d');
    }

    changeImgArr = (arr, exp = 1) => {
        arr = arr.map(e => new Array(exp).fill(e.map(ee => new Array(exp).fill(ee)).flat())).flat();
        let h = arr.length, w = arr[0].length;
        arr = arr.flat().flat();
        const img = new ImageData(Uint8ClampedArray.from(arr), w, h);
        this.context.putImageData(img, 0, 0);
    }

    render() {
        function rndArr(w, h) {
            return new Array(h).fill(0).map(
                () => new Array(w).fill(0).map(
                    () => new Array(4).fill(0).map(
                        () => Math.random() * 255)));
        }

        return (
            <>
                <canvas className="Canvas" ref={this.canvasRef} height={this.props.height} width={this.props.width}/>
                <br/>
                <button onClick={() => this.changeImgArr(rndArr(50, 50), 5)}>Change Img</button>
            </>
        );
    }
}
