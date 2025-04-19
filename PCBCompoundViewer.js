import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const simulatedPCBData = [
  {
    id: "PCB-118",
    name: "PCB 118",
    sdfUrl: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/35823/SDF",
    risk: "Moderate",
    organ: "Liver"
  },
  {
    id: "PCB-153",
    name: "PCB 153",
    sdfUrl: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/PCB-153/SDF",
    risk: "High",
    organ: "Nervous system"
  },
  {
    id: "PCB-180",
    name: "PCB 180",
    sdfUrl: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/37036/SDF",
    risk: "High",
    organ: "Endocrine system"
  },
  {
    id: "PCB-138",
    name: "PCB 138",
    sdfUrl: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/37035/SDF",
    risk: "Moderate",
    organ: "Reproductive system"
  },
  {
    id: "PCB-170",
    name: "PCB 170",
    sdfUrl: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/37037/SDF",
    risk: "High",
    organ: "Immune system"
  },
  {
    id: "PCB-126",
    name: "PCB 126",
    sdfUrl: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/63090/SDF",
    risk: "Very High",
    organ: "Skin and Liver"
  }
];

function PCBCompoundViewer() {
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const viewerRef = useRef(null);
  const viewerInstance = useRef(null);

  useEffect(() => {
    if (!window.$3Dmol) {
      const script = document.createElement("script");
      script.src = "https://3Dmol.org/build/3Dmol-min.js";
      script.onload = () => console.log("3Dmol.js loaded");
      document.body.appendChild(script);
    }
  }, []);

  useEffect(() => {
    if (selected && window.$3Dmol) {
      renderMolecule(selected);
    }
  }, [selected]);

  const renderMolecule = async (compound) => {
    setLoading(true);
    try {
      const res = await axios.get(compound.sdfUrl);
      if (viewerRef.current) {
        viewerRef.current.innerHTML = "";
        viewerInstance.current = window.$3Dmol.createViewer(viewerRef.current, {
          backgroundColor: "white"
        });
        viewerInstance.current.addModel(res.data, "sdf");
        viewerInstance.current.setStyle({}, { stick: {}, sphere: { scale: 0.3 } });
        viewerInstance.current.zoomTo();
        viewerInstance.current.zoom(0.8);
        viewerInstance.current.render();
        viewerInstance.current.zoomTo();
      }
    } catch (err) {
      console.error("Error rendering molecule", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "1rem" }}>PCB Compound Viewer</h1>

      <select
        onChange={(e) => {
          const compound = simulatedPCBData.find((c) => c.id === e.target.value);
          setSelected(compound);
        }}
        defaultValue=""
        style={{ padding: "0.5rem", marginBottom: "1.5rem" }}
      >
        <option value="">Select a PCB compound</option>
        {simulatedPCBData.map((compound) => (
          <option key={compound.id} value={compound.id}>
            {compound.name}
          </option>
        ))}
      </select>

      <div
  ref={viewerRef}
  style={{
    width: "100%",
    height: "500px",
    marginTop: "2rem",
    border: "1px solid #ccc",
    borderRadius: "1rem",
    overflow: "hidden", // <- this is the key
    backgroundColor: "white", // ensure canvas background is same
    position: "relative",
  }}
></div>


      {selected && (
        <div
          style={{
            backgroundColor: "#f0f8ff",
            padding: "1.5rem",
            borderRadius: "1rem",
            maxWidth: "300px",
            borderLeft: "5px solid #1e90ff"
          }}
        >
          <h2 style={{ marginBottom: "0.5rem" }}>{selected.name}</h2>
          <p>
            <strong>Risk Level:</strong> {selected.risk}
          </p>
          <p>
            <strong>Affects:</strong> {selected.organ}
          </p>
        </div>
      )}
    </div>
  );
}

export default PCBCompoundViewer;
