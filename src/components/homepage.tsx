import React, { useState } from 'react';
import { ShaderGradientCanvas, ShaderGradient } from '@shadergradient/react';
import "./homepage.css";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const Homepage: React.FC = () => {
  const [productLinks, setProductLinks] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setProductLinks(event.target.value);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!productLinks.trim()) {
      setError("Please enter an Amazon product link");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/reviewpages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          productLink: productLinks
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch reviews');
      }

      // Handle successful response
      console.log('Reviews:', data.reviews);
      // You can update state here to show the reviews

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
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
          <h1 className="mb-2 font-serif text-white text-7xl">ComparaSum</h1>
          <p className="slogan">Smart summaries, smarter decisions.</p>
        
          <div className="row">
            <Input
              type="text"
              placeholder="Paste your Amazon links here..."
              value={productLinks}
              onChange={handleInputChange}
              disabled={isLoading}
              className="flex-1 px-8 text-lg text-black bg-white border-none rounded-full h-14 placeholder:text-black/40"
            />
            <Button 
              onClick={handleSubmit}
              size="icon"
              disabled={isLoading}
              className="text-xl text-white bg-black rounded-full w-14 h-14 hover:bg-black/90"
            >
              {isLoading ? "..." : "→"}
            </Button>
          </div>
          {error && (
            <p className="mt-2 text-red-500">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Homepage;
