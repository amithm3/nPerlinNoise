import './dock.css'

function Dock() {
    return (
        <div className="Dock">
            <div className="Dock--primary">
                <h1>Dock Primary</h1>
            </div>
            <section className="PS--merge">
                <p>H1</p><p>H2</p>
            </section>
            <div className="Dock--secondary">
                <h1>Dock Secondary</h1>
            </div>
        </div>
    )
}

export default Dock
