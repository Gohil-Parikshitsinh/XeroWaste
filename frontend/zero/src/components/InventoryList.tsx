import React from 'react';
import { Clock, AlertTriangle, CheckCircle } from 'lucide-react';
import type { InventoryItem } from '../types';

interface InventoryListProps {
  items: InventoryItem[];
}

export function InventoryList({ items }: InventoryListProps) {
  const getStatusIcon = (status: InventoryItem['status']) => {
    switch (status) {
      case 'fresh':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'expiring-soon':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      case 'expired':
        return <AlertTriangle className="w-5 h-5 text-red-500" />;
    }
  };

  const getStatusClass = (status: InventoryItem['status']) => {
    switch (status) {
      case 'fresh':
        return 'bg-green-50 border-green-200';
      case 'expiring-soon':
        return 'bg-yellow-50 border-yellow-200';
      case 'expired':
        return 'bg-red-50 border-red-200';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-6">Detected Items</h2>
      <div className="space-y-4">
        {items.map((item) => (
          <div
            key={item.id}
            className={`p-4 rounded-lg border ${getStatusClass(item.status)} flex items-center justify-between`}
          >
            <div className="flex items-center space-x-4">
              {getStatusIcon(item.status)}
              <div>
                <h3 className="font-semibold">{item.name}</h3>
                <p className="text-sm text-gray-600">
                  Quantity: {item.quantity}
                  {item.expiryDate && ` • Expires: ${item.expiryDate}`}
                </p>
              </div>
            </div>
          </div>
        ))}
        {items.length === 0 && (
          <p className="text-gray-500 text-center py-8">
            No items detected. Try capturing your inventory!
          </p>
        )}
      </div>
    </div>
  );
}