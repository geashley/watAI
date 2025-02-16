import React, { useState } from 'react';
import { ShaderGradientCanvas, ShaderGradient } from '@shadergradient/react';
import "./homepage.css";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

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
    <div className="fixed inset-0 overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 z-0">
        <ShaderGradientCanvas
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            zIndex: -1, 
          }}
        >
          <ShaderGradient
            control="query"
            urlString="https://www.shadergradient.co/customize?animate=on&axesHelper=on&bgColor1=%23000000&bgColor2=%23000000&brightness=1.1&cAzimuthAngle=180&cDistance=2.9&cPolarAngle=115&cameraZoom=1&color1=%235606FF&color2=%23FE8989&color3=%23000000&destination=onCanvas&embedMode=off&envPreset=city&format=gif&fov=45&frameRate=10&grain=off&lightType=3d&pixelDensity=1&positionX=-0.5&positionY=0.1&positionZ=0&range=enabled&rangeEnd=40&rangeStart=0&reflection=0.1&rotationX=0&rotationY=0&rotationZ=235&shader=defaults&toggleAxis=false&type=waterPlane&uAmplitude=0&uDensity=1.1&uFrequency=5.5&uSpeed=0.1&uStrength=2.4&uTime=0.2&wireframe=false&zoomOut=false"
          />
        </ShaderGradientCanvas>
      </div>

      {/* Content */}
      <div className="content">
        <div className="text-container">
          <h1 className="font-serif text-white mmb-2 text-7xl">ComparaSum</h1>
          <p className="slogan">Smart summaries, smarter decisions.</p>
          
          <Card className="w-full max-w-2xl border-none shadow-2xl bg-white/10 backdrop-blur-md">
            <div className="row">
              <Input
                type="text"
                placeholder="Paste your Amazon links here..."
                value={productLinks}
                onChange={handleInputChange}
                className="flex-1 h-12 px-6 text-white border-none rounded-full bg-white/20 placeholder:text-white/60"
              />
              <Button 
                onClick={handleSubmit}
                size="icon"
                className="w-12 h-12 text-purple-900 bg-white rounded-full hover:bg-white/90"
              >
                →
              </Button>
            </div>
          </Card>
          </div>
      </div>
    </div>
  );
};

export default Homepage;
