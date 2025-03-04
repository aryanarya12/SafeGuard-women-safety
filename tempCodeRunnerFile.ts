import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import dynamic from "next/dynamic";

const Map = dynamic(() => import("@/components/Map"), { ssr: false });

export default function Dashboard() {
  const [cctvStatus, setCctvStatus] = useState("Idle");
  const [speed, setSpeed] = useState("Fetching...");
  const [alert, setAlert] = useState(null);

  const handleCCTVRecognition = async () => {
    setCctvStatus("Scanning...");
    const response = await fetch("/api/cctv");
    const data = await response.json();
    setCctvStatus(data.message || "Error");
  };

  const handleGPSSpeed = async () => {
    const response = await fetch("/api/gps");
    const data = await response.json();
    setSpeed(data.speed || "Error");
  };

  const handleSOS = async () => {
    const response = await fetch("/api/sos", { method: "POST" });
    const data = await response.json();
    setAlert(data.message);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">CCTV Face Recognition</h2>
          <p>Status: {cctvStatus}</p>
          <Button onClick={handleCCTVRecognition}>Start Recognition</Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">GPS Speed Tracking</h2>
          <p>Speed: {speed}</p>
          <Button onClick={handleGPSSpeed}>Check Speed</Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">SOS Emergency Alert</h2>
          <p>{alert || "Press the button to send an alert"}</p>
          <Button onClick={handleSOS} className="bg-red-500">Trigger SOS</Button>
        </CardContent>
      </Card>

      <Card className="col-span-2">
        <CardContent>
          <h2 className="text-xl font-bold">Hotspot Mapping</h2>
          <Map />
        </CardContent>
      </Card>
    </div>
  );
}
