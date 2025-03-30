import React, { useState } from 'react';
import { Camera } from './components/Camera';
import { InventoryList } from './components/InventoryList';
import { InventoryStats } from './components/InventoryStats';
import { ScanBarcode } from 'lucide-react';
import type { InventoryItem } from './types';

const calculateStats = (items: InventoryItem[]) => {
  return {
    totalItems: items.reduce((sum, item) => sum + item.quantity, 0),
    freshItems: items.filter(item => item.status === 'fresh')
      .reduce((sum, item) => sum + item.quantity, 0),
    expiringSoonItems: items.filter(item => item.status === 'expiring-soon')
      .reduce((sum, item) => sum + item.quantity, 0),
    expiredItems: items.filter(item => item.status === 'expired')
      .reduce((sum, item) => sum + item.quantity, 0),
  };
};

// Simulated detection results for demo purposes
const mockDetection = async (imageSrc: string): Promise<InventoryItem[]> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  return [
    {
      id: '1',
      name: 'Apples',
      quantity: 5,
      expiryDate: '2024-03-25',
      status: 'fresh'
    },
    {
      id: '2',
      name: 'Milk',
      quantity: 1,
      expiryDate: '2024-03-20',
      status: 'expiring-soon'
    },
    {
      id: '3',
      name: 'Bread',
      quantity: 1,
      expiryDate: '2024-03-15',
      status: 'expired'
    }
  ];
};

function App() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const stats = calculateStats(items);

  const handleCapture = async (imageSrc: string) => {
    setIsProcessing(true);
    try {
      const detectedItems = await mockDetection(imageSrc);
      setItems(detectedItems);
    } catch (error) {
      console.error('Error processing image:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-3">
            <ScanBarcode className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">
              Smart Inventory Management
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="space-y-8">
          <InventoryStats stats={stats} />
          <div className="grid gap-8 md:grid-cols-2">
            <div>
              <Camera onCapture={handleCapture} isProcessing={isProcessing} />
            </div>
            <div>
              <InventoryList items={items} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;