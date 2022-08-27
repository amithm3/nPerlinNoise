import './dock.css'

function domID(id) {
    return document.getElementById(id)
}

function newNoise() {
    let freq = domID('Frequencyinp').value, seed = domID('Seedinp').value, wLen = domID('WaveLengthinp').value
    let _oct = domID('Octavesinp').value, _lac = domID('Lacunarityinp').value, _per = domID('Persistenceinp').value
    console.log(freq, seed, wLen, _oct, _lac, _per)
    if(seed < 0) seed = 'None'
    window.pyodide.runPython("newNoise(" + freq + ',' + seed + ',' + wLen + ',(0, 1),' + _oct + ',' + _lac + ',' + _per + ",dims=2); print(noises)")
}

function LInp(props) {
    let name = props['name'], text = props['text']
    if (!text) text = name
    return (
        <section id={name + '-sec'}>
            <label htmlFor={name} id={name + 'lab'}>{text}: </label>
            <input {...props} id={name + 'inp'}/>
        </section>
    )
}

function rangeOnX(name, toFixed = 0) {
    let lab = domID(name + 'lab'), inp = domID(name + 'inp')
    lab.innerText = inp.name + ' (' + parseFloat(inp.value).toFixed(toFixed) + ')'
}

function PDock() {
    return (
        <div className="Dock--primary">
            <LInp name="Frequency" type="number" defaultValue="8" min="2"/>
            <LInp name="Seed" type="number" defaultValue="-1" min="-1" step="1"
                  onChange={(e) => e.target.value = (e.target.value < -1) ? -1 : e.target.value !== '' ? e.target.value : -1}/>
            <LInp name="WaveLength" type="number" defaultValue="128" min="2" step="2"
                  onChange={(e) => e.target.value = (e.target.value < 2) ? 2 : e.target.value}/>
            <LInp name="Octaves" type="range" defaultValue="8" min="1" max="8"
                  onChange={() => rangeOnX('Octaves')} text="Octaves (8)"/>
            <LInp name="Lacunarity" type="range" defaultValue="2" min="2" max="4"
                  onChange={() => rangeOnX('Lacunarity')} text="Lacunarity (2)"/>
            <LInp name="Persistence" type="range" defaultValue="0.5" min="0" max="1" step=".01"
                  onChange={() => rangeOnX('Persistence', 2)} text="Persistence (0.50)"/>
            <input type="button" onClick={newNoise} value="Click"/>
        </div>
    )
}

function Dock() {
    return (
        <div className="Dock">
            <PDock/>
            <section className="PS--merge">
                <p>Dock Primary</p><p>Dock Secondary</p>
            </section>
            <div className="Dock--secondary">
            </div>
        </div>
    )
}

export default Dock
