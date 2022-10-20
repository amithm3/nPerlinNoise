import { useState } from "react";

import "./noise.scss";

const Noise = () => {
  const [enteredOctave, setOctave] = useState("");
  const [enteredPersistance, setPersistance] = useState("");
  const [enteredlacunarity, setlacunarity] = useState("");
  const [enteredSeed, setSeed] = useState("");
  const [enteredFrequency, setFrequency] = useState("");
  const [enteredWavelength, setWavelength] = useState("");
  const [enteredWarp, setWarp] = useState("");
  const [enteredRange, setRange] = useState("");

  const [isActive, setIsActive] = useState(false);

  const OctaveChange = (e) => {
    setOctave(e.target.value);
    console.log(e.target.value);
  };
  const PersistanceChange = (e) => {
    setPersistance(e.target.value);
    console.log(e.target.value);
  };
  const lacunarityChange = (e) => {
    setlacunarity(e.target.value);
    console.log(e.target.value);
  };
  const SeedChange = (e) => {
    setSeed(e.target.value);
    console.log(e.target.value);
  };
  const FrequencyChange = (e) => {
    setFrequency(e.target.value);
    console.log(e.target.value);
  };
  const WavelengthChange = (e) => {
    setWavelength(e.target.value);
    console.log(e.target.value);
  };
  const WarpChange = (e) => {
    setWarp(e.target.value);
    console.log(e.target.value);
  };
  const RangeChange = (e) => {
    setRange(e.target.value);
    console.log(e.target.value);
  };

  const submitHandler = (event) => {
    event.preventDefault();
    setOctave("");
    setPersistance("");
    setlacunarity("");
    setFrequency("");
    setSeed("");
    setWavelength("");
    setWarp("");
    setRange(" ");
  };

  return (
    <div className="noise">
      <button className="noise-btn" onClick={(e) => setIsActive(!isActive)}>
        Customize the image setting
      </button>
      {isActive && (
        <form className="form" onSubmit={submitHandler}>
          <label className="label">Octaves</label>
          <div className="field">
            <span>{enteredOctave}</span>
            <input
              type={"range"}
              className="input"
              max="8"
              min="1"
              step="1"
              onChange={OctaveChange}
              value={enteredOctave}
            ></input>
          </div>
          <label className="label">Persistance</label>
          <div className="field">
            <span>{enteredPersistance}</span>
            <input
              type={"range"}
              className="input"
              max="1"
              min="0.00"
              step="0.01"
              onChange={PersistanceChange}
              value={enteredPersistance}
            ></input>
          </div>
          <label className="label">lacunarity</label>
          <input
            type={"range"}
            className="input"
            onChange={lacunarityChange}
            value={enteredlacunarity}
          ></input>

          <label className="label">Seed</label>
          <input
            type={"number"}
            className="input"
            onChange={SeedChange}
            value={enteredSeed}
          ></input>

          <label className="label">Frequency</label>
          <div className="field">
            <span>{enteredFrequency}</span>
            <input
              type={"range"}
              max="32"
              min="1"
              step="1"
              className="input"
              onChange={FrequencyChange}
              value={enteredFrequency}
            ></input>
          </div>

          <label className="label">Wavelength</label>
          <div className="field">
            <span>{enteredWavelength}</span>
            <input
              type={"range"}
              min="0.00"
              step="0.01"
              className="input"
              onChange={WavelengthChange}
              value={enteredWavelength}
            ></input>
          </div>

          <label className="label">Warp</label>
          <input
            type={"range"}
            className="input"
            onChange={WarpChange}
            value={enteredWarp}
          ></input>
          <label className="label">Range</label>
          <input type={"text"} className="input" value={enteredRange}></input>

          <button type="submit">Apply Changes</button>
        </form>
      )}
    </div>
  );
};

export default Noise;
