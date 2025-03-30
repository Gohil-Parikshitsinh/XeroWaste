import React, { useCallback, useRef } from 'react';
import Webcam from 'react-webcam';
import { Camera as CameraIcon, RefreshCw } from 'lucide-react';

interface CameraProps {
  onCapture: (imageSrc: string) => void;
  isProcessing: boolean;
}

export function Camera({ onCapture, isProcessing }: CameraProps) {
  const webcamRef = useRef<Webcam>(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      onCapture(imageSrc);
    }
  }, [onCapture]);

  return (
    <div className="relative rounded-lg overflow-hidden shadow-lg bg-white">
      <Webcam
        ref={webcamRef}
        audio={false}
        screenshotFormat="image/jpeg"
        className="w-full h-[400px] object-cover"
      />
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <button
          onClick={capture}
          disabled={isProcessing}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-full flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          {isProcessing ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              <span>Processing...</span>
            </>
          ) : (
            <>
              <CameraIcon className="w-5 h-5" />
              <span>Capture Inventory</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}