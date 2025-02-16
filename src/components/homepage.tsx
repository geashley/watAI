import React, { useState } from 'react';
import { ShaderGradientCanvas, ShaderGradient } from '@shadergradient/react';
import "./homepage.css";

const Homepage: React.FC = () => {
  const [productLinks, setProductLinks] = useState("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setProductLinks(event.target.value);
  };

  const handleSubmit = () => {
    console.log("Submitted links:", productLinks);
    // Implement logic for processing the links
  };

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      <ShaderGradientCanvas
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
        }}
      >
        <ShaderGradient
          control="query"
          urlString="https://www.shadergradient.co/customize?animate=on&axesHelper=on&bgColor1=%23000000&bgColor2=%23000000&brightness=1.1&cAzimuthAngle=180&cDistance=2.9&cPolarAngle=115&cameraZoom=1&color1=%235606FF&color2=%23FE8989&color3=%23000000&destination=onCanvas&embedMode=off&envPreset=city&format=gif&fov=45&frameRate=10&grain=off&lightType=3d&pixelDensity=1&positionX=-0.5&positionY=0.1&positionZ=0&range=enabled&rangeEnd=40&rangeStart=0&reflection=0.1&rotationX=0&rotationY=0&rotationZ=235&shader=defaults&toggleAxis=false&type=waterPlane&uAmplitude=0&uDensity=1.1&uFrequency=5.5&uSpeed=0.1&uStrength=2.4&uTime=0.2&wireframe=false&zoomOut=false"
        />
      </ShaderGradientCanvas>
      <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: 'white', textAlign: 'center' }}>
        <h1 className="font-semibold text-4xl">ComparaSum</h1>
        <input
          type="text"
          placeholder="Paste your Amazon product links here!."
          value={productLinks}
          onChange={handleInputChange}
          className="w-[10000px] p-[1500px] rounded-full text-white bg-purple-900 border-none outline-none placeholder-gray-300"
        />
        <br />
        <button
          onClick={handleSubmit}
          className="mt-4 px-6 py-3 bg-white text-purple-900 font-semibold rounded-full shadow-md hover:bg-gray-200 transition"
        >
          Compare
        </button>
      </div>
    </div>
  );
};

export default Homepage;
