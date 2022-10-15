import './Glass.css';

function Glass({children, back, ...props}) {
    return (
        <div className="Glass--cnt">
            <div className="Glass" {...props}>{children}</div>
            <div className="Glass-back">{back}</div>
        </div>
    );
}

function Circle({children, bg, x, y, nx, ny, w, h, style, ...props}) {
    return (
        <div className="Circle" {...props}
             style={{
                 background: bg,
                 left: x,
                 right: nx,
                 top: y,
                 bottom: ny,
                 width: w,
                 height: h,
                 ...style
             }}>
            {children}
        </div>
    );
}

export {Glass, Circle}
