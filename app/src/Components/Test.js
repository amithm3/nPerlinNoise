import './Table.css';

function Table({children, widths=[50, 30]}) {
    let newChildren = [];
    for (let row of children) {
        if (row.type === TableRow) {
            row = <row.type {...row.props} widths={widths}/>
        }
        newChildren.push(row);
    }
    return (
        <div className="Table">
            {newChildren}
        </div>
    );
}

function TableRow({children, widths}) {
    let newChildren = [], i = 0;
    for (let cell of children) {
        if (cell.type === TableCell) {
            cell = <cell.type {...cell.props} width={i < widths.length ? widths[i] : widths[widths.length - 1]}/>
        }
        newChildren.push(cell)
        i++;
    }
    return (
        <span className="Table--Row">
            {newChildren}
        </span>
    );
}

function TableCell({children, width}) {
    return (
        <div className="Table--Cell" style={{width: width}}>
            {children}
        </div>
    );
}

export default function Test() {
    const table = createData(
        createData("...", 0, 0, 0, 0),
        createData(1, 1, 1, 1, 1),
        createData(2, 2, 2, 2, 2),
        createData(3, 3, 3, 3, 3),
        createData(4, 4, 4, 4, 4),
        createData(5, 5, 5, 5, 5),
    )
    let row = 0, col = 0;
    return (
        <>
            <Table>
                {table.map(r => <TableRow key={row++}>{r.map(v => <TableCell key={col++}>{v}</TableCell>)}</TableRow>)}
            </Table>
        </>
    );
}

function createData(...args) {
    return [...args]
}
