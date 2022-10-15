import './ImgPort.css';
import DImg from "../components/DImg/DImg";

export default class extends DImg {
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
